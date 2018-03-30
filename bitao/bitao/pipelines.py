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
            cursor.execute(
                " insert reptile_source(content,publisher_nicke_name,publisher_real_name,publisher_avatar,publish_time,publisher_identifier"
                ",publisher_desc,source_platform,source_address,content_id) "
                " VALUES (%(content)s,%(publisher_nicke_name)s,%(publisher_real_name)s "
                ",%(publisher_avatar)s,%(publish_time)s,%(publisher_identifier)s,%(publisher_desc)s  "
                ",%(source_platform)s,%(source_address)s,%(content_id)s  )",
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
    def filter_emoji(self,desstr):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub("", desstr)


