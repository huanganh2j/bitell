# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import json
import  re
import sys
from twisted.enterprise import adbapi
reload(sys)
sys.setdefaultencoding('utf-8')
class BitaoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            # cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        item = dict(item)
        cursor.execute(" select count(*) as count from reptile_source where content_id='" + item["content_id"] + "' ")
        count_data=cursor.fetchone()
        if count_data[0]>0:
            print item["content_id"]+"已经爬取过了"
        else:

            # 保存微博正文
            cursor.execute(
                " insert reptile_source(content,publisher_nicke_name,publisher_real_name,publisher_avatar,publish_time,publisher_identifier"
                ",publisher_desc,source_platform,source_address,content_id) "
                " VALUES (%(content)s,%(publisher_nicke_name)s,%(publisher_real_name)s "
                ",%(publisher_avatar)s,%(publish_time)s,%(publisher_identifier)s,%(publisher_desc)s  "
                ",%(source_platform)s,%(source_address)s,%(content_id)s )",
                {"content": self.filter_emoji(item["content"]).encode('utf-8') if item.has_key("content") else "",
                 "publisher_nicke_name": item["publisher_nicke_name"] if item.has_key("publisher_nicke_name") else "",
                 "publisher_real_name": ""
                    , "publisher_avatar": item["publisher_avatar"] if item.has_key("publisher_avatar") else "",
                 "publish_time": item["publish_time"] if item.has_key("publish_time") else "",
                 "publisher_identifier": item["publisher_identifier"] if item.has_key("publisher_identifier") else "",
                 "publisher_desc": item["publisher_desc"] if item.has_key("publisher_desc") else "微博 weibo.com",
                 "source_platform": item["source_platform"] if item.has_key("source_platform") else "",
                 "source_address": item["source_address"] if item.has_key("source_address") else "",
                 "content_id": item["content_id"] if item.has_key("content_id") else ""
                 })

            cursor.execute(" select id from reptile_source where content_id='" + item["content_id"] + "' limit 1 ")
            queryData = cursor.fetchone()
            if len(item["pics"]):
                pics = item["pics"]
                sortindex = 1
                for pic in pics:
                    small = pic["url"]
                    large = pic["large"]["url"]
                    cursor.execute("insert into reptile_source_pics(reptile_source_id,pic_url,big_pic_url,position_sort) VALUES "
                                   "(%(reptile_source_id)s,%(pic_url)s,%(big_pic_url)s,%(sort)s)",
                                   {"reptile_source_id": queryData[0], "pic_url": small, "big_pic_url": large,
                                    "sort": sortindex})
                    sortindex = sortindex + 1
            if len(item["page_info"]):
                page_info = item["page_info"]
                video_url=page_info["page_url"]
                cover_image_url = page_info["page_pic"]["url"]
                cursor.execute(
                    "insert into reptile_source_video(reptile_source_id,video_url,cover_image_url) VALUES "
                    "(%(reptile_source_id)s,%(video_url)s,%(cover_image_url)s )",
                    {"reptile_source_id": queryData[0], "video_url": video_url, "cover_image_url": cover_image_url
                     })

            etweeted_id = None
            # 保存转发内容
            if item["retweeted_status"] is not None and len(item["retweeted_status"]):
                etweeted_status = item["retweeted_status"]
                # 被转发微博的id
                id = etweeted_status["id"]
                etweeted_id = id
                # 被转发微博的发布时间
                created_at = etweeted_status["created_at"]
                # 被转发微博的内容
                text = etweeted_status["text"]
                user = etweeted_status["user"]
                screen_name = user["screen_name"]
                user_id = user["id"]
                verified_reason = user["verified_reason"] if user.has_key("verified_reason") else ""
                description = user["description"] if user.has_key("description") else ""
                avatar_hd = user["avatar_hd"] if user.has_key("avatar_hd") else ""
                source_address = "https://m.weibo.cn/status/" + id
                weibo_desc = None
                if verified_reason is not None and len(verified_reason):
                    weibo_desc = verified_reason
                if description is not None and len(description):
                    weibo_desc = description;
                cursor.execute(
                    " insert source_fowards(reptile_source_id,content,publisher_nicke_name,publisher_real_name,publisher_avatar,publish_time,"
                    "publisher_identifier"
                    ",publisher_desc,source_platform,source_address,content_id) "
                    " VALUES (%(reptile_source_id)s,%(content)s,%(publisher_nicke_name)s,%(publisher_real_name)s "
                    ",%(publisher_avatar)s,%(publish_time)s,%(publisher_identifier)s,%(publisher_desc)s  "
                    ",%(source_platform)s,%(source_address)s,%(content_id)s )",
                    {"reptile_source_id":queryData[0],"content": self.filter_emoji(text).encode('utf-8') if text is not None else "",
                     "publisher_nicke_name": screen_name if screen_name is not None else "",
                     "publisher_real_name": ""
                        , "publisher_avatar": avatar_hd if avatar_hd is not None else "",
                     "publish_time": created_at if created_at is not None else "",
                     "publisher_identifier": user_id if user_id is not None else "",
                     "publisher_desc": weibo_desc if weibo_desc is not None else "",
                     "source_platform": "weibo",
                     "source_address": source_address if source_address is not None else "",
                     "content_id": id if id is not None else ""
                     })
                cursor.execute(" select id from source_fowards where content_id='" + id + "' limit 1 ")
                etweeted_data_id = cursor.fetchone()
                # 保存转发微博图片
                if etweeted_status.has_key("pics"):
                    etweeted_pics = etweeted_status["pics"]
                    etweeted_pic_index = 1
                    for etweeted_pic in etweeted_pics:
                        etweeted_small = etweeted_pic["url"]
                        etweeted_large = etweeted_pic["large"]["url"]
                        cursor.execute(
                            "insert into source_fowards_pics(source_fowards_id,pic_url,big_pic_url,position_sort) VALUES "
                            "(%(source_fowards_id)s,%(pic_url)s,%(big_pic_url)s,%(sort)s)",
                            {"source_fowards_id": etweeted_data_id[0], "pic_url": etweeted_small,
                             "big_pic_url": etweeted_large,
                             "sort": etweeted_pic_index})
                        etweeted_pic_index = etweeted_pic_index + 1
                # 保存转发微博的视频
                if etweeted_status.has_key("page_info"):
                    etweeted_page_info = etweeted_status["page_info"]
                    etweeted_cover_image_url = etweeted_page_info["page_pic"]["url"]
                    etweeted_video_url = etweeted_page_info["page_url"]
                    cursor.execute(
                        "insert into source_fowards_video(source_fowards_id,video_url,cover_image_url) VALUES "
                        "(%(source_fowards_id)s,%(video_url)s,%(cover_image_url)s )",
                        {"source_fowards_id": etweeted_data_id[0], "video_url": etweeted_video_url,
                         "cover_image_url": etweeted_cover_image_url
                         })

    def filter_emoji(self,desstr):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub("", desstr)


