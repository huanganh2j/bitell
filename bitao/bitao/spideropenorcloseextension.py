# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy import cmdline
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
import time
from scrapy.exceptions import NotConfigured
import MySQLdb
class SpiderOpenCloseLogging(object):
    def __init__(self):
        super(SpiderOpenCloseLogging, self).__init__()

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self, spider):
        settings = get_project_settings()
        print "spider "+spider.id+"关闭信号接收"
        conn = MySQLdb.Connect(host=settings["MYSQL_HOST"], port=3306, user=settings["MYSQL_USER"], passwd=settings["MYSQL_PASSWORD"], db=settings["MYSQL_DBNAME"],
                               charset='UTF8');
        cursor = conn.cursor()
        # 修改处理状态
        cursor.execute(" update weibo_target_list set is_handle=1 ")
        conn.commit()
        cursor.close()
        conn.close()
        # if spider.name=="jinse":
        #     cmdline.execute(
        #         "scrapy runspider C:/Users/huangan/PycharmProjects/bitell/bitao/bitao/spiders/weibosecondspider.py".split())