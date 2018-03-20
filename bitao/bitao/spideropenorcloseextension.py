# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy import cmdline
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
        print "spider "+spider.id+"关闭信号接收"
        conn = MySQLdb.Connect(host='localhost', port=3306, user='root', passwd='923469an', db='reptile_metadata',
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