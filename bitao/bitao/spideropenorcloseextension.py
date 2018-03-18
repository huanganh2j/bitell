# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy import cmdline
from twisted.internet import reactor, defer
import time
from scrapy.exceptions import NotConfigured
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
        # if spider.name=="jinse":
        #     cmdline.execute(
        #         "scrapy runspider C:/Users/huangan/PycharmProjects/bitell/bitao/bitao/spiders/weibosecondspider.py".split())