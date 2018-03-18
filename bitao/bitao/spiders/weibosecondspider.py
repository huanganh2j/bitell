# -*- coding: utf-8 -*-
import scrapy
import time
import re
import sys
from scrapy.http.cookies import CookieJar
import json

from selenium import webdriver

from bitao.items import BitaoItem
reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboSecondSpider(scrapy.Spider):
    name = 'weibosecond'
    id="weibosecond"
    ulrstr= "https://m.weibo.cn/api/container/getIndex?uid=5546018379&luicode=10000011&lfid=100103type%3D3%26q%3DBTC123%E5%BC%A0%E6%B7%9E%E7%9A%93Ricardo&featurecode=20000320&type=user&containerid=1076035546018379&page="
    start_urls = [ulrstr+"1"]
    def __init__(self):
        print "weibosecond spider 启动了"
        # self.browser = webdriver.Chrome(executable_path="E:/toolsource/pythontoolsource/chromedriver.exe")
        self.pageIndex=1
        self.requestUrl="https://m.weibo.cn/api/container/getIndex?uid=5546018379&luicode=10000011&lfid=100103type%3D3%26q%3DBTC123%E5%BC%A0%E6%B7%9E%E7%9A%93Ricardo&featurecode=20000320&type=user&containerid=1076035546018379&page="
        super(WeiboSecondSpider,self).__init__()

    def parse(self,response):
        responsestr = str(response.body)
        responsestr_h =self.filter_emoji(responsestr)
        print responsestr_h
        self.pageIndex=self.pageIndex+1
        result =json.loads(responsestr_h,encoding="utf-8")
        if result["ok"]!=1 :
            return
        # 得到data
        data =result["data"]
        if len(data) :
            cards = data["cards"]
            # 得到每个card
            for card in cards:
                item = BitaoItem()
                # 微博详情地址
                item["source_address"] =card["scheme"]
                # 得到微博内容
                mblog=card["mblog"]
                item["publish_time"]=mblog["created_at"]
                item["content"]=mblog["text"]
                print (mblog["text"])
                item["source_platform"]="weibo"
                # 得到发布者信息
                user =mblog["user"]
                item["publisher_identifier"]=user["id"]
                item["publisher_nicke_name"]=user["screen_name"]
                item["publisher_avatar"]=user["avatar_hd"]
                item["publisher_desc"]=user["verified_reason"]
                # 得到图片对象
                try:
                    pics =mblog["pics"]
                    item["pics"]=pics
                except KeyError:
                    print("该微博没有图片")
                    item["pics"] = ""
                yield item
            yield scrapy.Request(
               "https://m.weibo.cn/api/container/getIndex?uid=5546018379&luicode=10000011&lfid=100103type%3D3%26q%3DBTC123%E5%BC%A0%E6%B7%9E%E7%9A%93Ricardo&featurecode=20000320&type=user&containerid=1076035546018379&page="+str(self.pageIndex),
                    callback=self.parse)
        else:
            return


    def filter_emoji(self,desstr):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub("", desstr)
    def start_requests(self):
        for url in self.start_urls:
            # yield scrapy.Request(url, cookies={'SUB=_2A253raVjDeRhGeNK7VAU9ibMyj-IHXVVUcsrrDV6PUJbkdAKLRHykW1NSTHSoRqOG_DS9sEmxXsav5R4qIkjW2JY; SUHB=0G0u6ey9_1-kHJ; SCF=AouotuoUWHGbf-lZy9F9XklNFHI2Cg02MgnGV5XKigVYq3AFp-Ypm7NdZI5Rkcx6N4BbeENGS9prGdXxn81MGBM.; SSOLoginState=1521079603; _T_WM=384bcb04b69ecf26cfa6fdb186fec5a3; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword%26fid%3D1076032145291155%26uicode%3D10000011': 'true'})
            yield scrapy.Request(url, meta = {'cookiejar' : 1})