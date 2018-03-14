# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver

class JinseSpider(scrapy.Spider):
    name = 'jinse'
    allowed_domains = ['https://weibo.com/']
    start_urls = ['https://weibo.com/']
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="E:/toolsource/pythontoolsource/chromedriver.exe")
        super(JinseSpider,self).__init__()
    def parse(self, response):
        print response.body
         # jinseitems =response.xpath('//ol [@class="list clearfix"]').extract()
         # for jinseitem in jinseitems :
         #     print jinseitem +"\n"
