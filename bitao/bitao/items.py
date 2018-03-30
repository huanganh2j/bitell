# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class BitaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    publisher_nicke_name = scrapy.Field()
    publisher_real_name = scrapy.Field()
    publisher_avatar = scrapy.Field()
    publish_time = scrapy.Field()
    publisher_identifier = scrapy.Field()
    publisher_desc = scrapy.Field()
    source_platform = scrapy.Field()
    source_address = scrapy.Field()
    content_id = scrapy.Field()
    pics=scrapy.Field()
    page_info=scrapy.Field()
    retweeted_status = scrapy.Field()
