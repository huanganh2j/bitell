# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver

class JinseSpider(scrapy.Spider):
    name = 'jinse'
    # allowed_domains = ['https://weibo.com/']
    start_urls = ['https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F']
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="E:/toolsource/pythontoolsource/chromedriver.exe")
        super(JinseSpider,self).__init__()
    def parse(self, response):
        return scrapy.Request("https://m.weibo.cn/u/2145291155?uid=2145291155",callback=self.parseUser)
        # print response.body
         # jinseitems =response.xpath('//ol [@class="list clearfix"]').extract()
         # for jinseitem in jinseitems :
         #     print jinseitem +"\n"

    def parseUser(self, response):
        return scrapy.Request("https://m.weibo.cn/api/container/getIndex?uid=2145291155&type=uid&value=2145291155&containerid=1076032145291155&page=100", callback=self.parseUserWeibo)
        # jinseitems =response.xpath('//ol [@class="list clearfix"]').extract()
        # for jinseitem in jinseitems :
        #     print jinseitem +"\n"
    def parseUserWeibo(self,response):
        print response.body

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies={'SUB=_2A253raVjDeRhGeNK7VAU9ibMyj-IHXVVUcsrrDV6PUJbkdAKLRHykW1NSTHSoRqOG_DS9sEmxXsav5R4qIkjW2JY; SUHB=0G0u6ey9_1-kHJ; SCF=AouotuoUWHGbf-lZy9F9XklNFHI2Cg02MgnGV5XKigVYq3AFp-Ypm7NdZI5Rkcx6N4BbeENGS9prGdXxn81MGBM.; SSOLoginState=1521079603; _T_WM=384bcb04b69ecf26cfa6fdb186fec5a3; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword%26fid%3D1076032145291155%26uicode%3D10000011': 'true'})