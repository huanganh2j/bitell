# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import json
import  re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
class BitaoPipeline(object):
    def process_item(self, item, spider):
        # try:
            conn = MySQLdb.Connect(host='localhost', port=3306, user='root', passwd='923469an', db='reptile_metadata',
                                   charset='UTF8');
            cursor = conn.cursor();
            item=dict(item)
            if len(item["pics"]) :
                pics =item["pics"]
                for pic in pics:
                    small = pic["url"]
                    large = pic["large"]["url"]
            cursor.execute(" insert reptile_source(content,publisher_nicke_name,publisher_real_name,publisher_avatar,publish_time,publisher_identifier"
                           ",publisher_desc,source_platform,source_address) "
                           " VALUES (%(content)s,%(publisher_nicke_name)s,%(publisher_real_name)s "
                           ",%(publisher_avatar)s,%(publish_time)s,%(publisher_identifier)s,%(publisher_desc)s  "
                           ",%(source_platform)s,%(source_address)s  )",{"content":self.filter_emoji(item["content"]).encode('utf-8') if item.has_key("content") else "",
                            "publisher_nicke_name":item["publisher_nicke_name"] if item.has_key("publisher_nicke_name") else "",
                                                                         "publisher_real_name":""
                            ,"publisher_avatar":item["publisher_avatar"] if item.has_key("publisher_avatar") else "",
                                                                         "publish_time":item["publish_time"] if item.has_key("publish_time") else "",
                                                                         "publisher_identifier": item["publisher_identifier"] if item.has_key("publisher_identifier") else "",
                                                                         "publisher_desc": item["publisher_desc"] if item.has_key("publisher_desc") else "微博 weibo.com",
                                                                         "source_platform": item["source_platform"] if item.has_key("source_platform") else "",
                                                                         "source_address": item["source_address"] if item.has_key("source_address") else ""
                                                                         })
            conn.commit();
            cursor.close();
            conn.close();
            return item
        # except:
        #     print Error
        #     print("管道处理数据异常")
        #     return item
    def filter_emoji(self,desstr):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub("", desstr)


