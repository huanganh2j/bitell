# -*- coding: utf-8 -*-
import scrapy
import time
import re
import sys
from scrapy.http.cookies import CookieJar
import json
import datetime
from selenium import webdriver

from bitao.items import BitaoItem
# reload(sys)
# sys.setdefaultencoding('utf-8')
from bitao.targetsource import TargetSource


class JinseSpider(scrapy.Spider):
    name = 'jinse'
    id="weibo"
    # allowed_domains = ['https://weibo.com/']
    start_urls = ['https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F']
    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="E:/toolsource/pythontoolsource/chromedriver.exe")
        self.pageIndex=1
        self.target_url=""
        super(JinseSpider,self).__init__()
    def parse(self, response):
        self.target_url =TargetSource.getTarget()
        if len(self.target_url):
            return scrapy.Request(
                self.target_url+str(self.pageIndex),
                callback=self.parseUserWeibo)
        else:
            print "没有获取到爬取目标"
            return

    # def parseUser(self, response):
    #     return scrapy.Request("https://m.weibo.cn/api/container/getIndex?uid=2145291155&type=uid&value=2145291155&containerid=1076032145291155&page=8", callback=self.parseUserWeibo)
        # jinseitems =response.xpath('//ol [@class="list clearfix"]').extract()
        # for jinseitem in jinseitems :
        #     print jinseitem +"\n"
    def parseUserWeibo(self,response):
        responsestr = str(response.body)
        responsestr_h =self.filter_emoji(responsestr)
        print responsestr_h
        self.pageIndex=self.pageIndex+1
        result =json.loads(responsestr_h,encoding="utf-8")
        if result["ok"]!=1 :
            self.pageIndex = 1
            print "进行下一个目标爬取"
            self.target_url = TargetSource.getTarget()
            if len(self.target_url):
                yield scrapy.Request(
                    self.target_url + str(self.pageIndex),
                    callback=self.parseUserWeibo)
            else:
                print "没有获取到爬取目标"
                return
        # 得到data
        donext=False
        data =result["data"]
        if len(data) :
            cards = data["cards"]
            # 得到每个card
            for card in cards:
                if card["card_type"]!= 9:
                    continue;
                item = BitaoItem()
                item["content_id"]=card["itemid"]
                # 微博详情地址
                item["source_address"] =card["scheme"]
                # 得到微博内容
                mblog=card["mblog"]
                publish_time = mblog["created_at"]
                if publish_time is not None and len(publish_time):
                    # publish_time=publish_time.encode("utf8")
                    timestr = publish_time.split('-')
                    publishDateTime=None
                    now =datetime.datetime.now()
                    if len(timestr)==2:
                        year = now.year
                        publishDateTime = datetime.datetime(year, int(str(timestr[0])), int(str(timestr[1])))
                        intertime = (now - publishDateTime).days
                        if intertime > 1:
                            # 如果爬取内容时间 距离当前时间1天则不再爬取 ，直接进入下一个爬取目标
                            donext=True
                            break
                            # self.pageIndex = 1
                            # print "进行下一个目标爬取"
                            # self.target_url = TargetSource.getTarget()
                            # if len(self.target_url):
                            #     yield scrapy.Request(
                            #         self.target_url + str(self.pageIndex),
                            #         callback=self.parseUserWeibo)
                            # else:
                            #     print "没有获取到爬取目标"
                            #     return
                    elif len(timestr)==3:
                        publishDateTime = datetime.datetime(int(str(timestr[0])), int(str(timestr[1])), int(str(timestr[2])))
                        intertime = (now - publishDateTime).days
                        if intertime > 1:
                            # 如果爬取内容时间 距离当前时间1天则不再爬取 ，直接进入下一个爬取目标
                            donext = True
                            break
                            # self.pageIndex = 1
                            # print "进行下一个目标爬取"
                            # self.target_url = TargetSource.getTarget()
                            # if len(self.target_url):
                            #     yield scrapy.Request(
                            #         self.target_url + str(self.pageIndex),
                            #         callback=self.parseUserWeibo)
                            # else:
                            #     print "没有获取到爬取目标"
                            #     return
                    item["publish_time"]=publish_time
                item["content"]=mblog["text"]
                # print (mblog["text"])
                item["source_platform"]="weibo"
                # 得到发布者信息
                user =mblog["user"]
                item["publisher_identifier"]=user["id"]
                item["publisher_nicke_name"]=user["screen_name"]
                item["publisher_avatar"]=user["avatar_hd"]
                if user.has_key("verified_reason"):
                    item["publisher_desc"]=user["verified_reason"]
                if user.has_key("description"):
                    item["publisher_desc"] = user["description"]
                # 得到图片对象
                try:
                    pics =mblog["pics"]
                    item["pics"]=pics
                except KeyError:
                    print("该微博没有图片")
                    item["pics"] = ""
                yield item
            if donext==True:
                self.pageIndex = 1
                print "进行下一个目标爬取"
                self.target_url = TargetSource.getTarget()
                if len(self.target_url):
                    yield scrapy.Request(
                        self.target_url + str(self.pageIndex),
                        callback=self.parseUserWeibo)
                else:
                    print "没有获取到爬取目标"
                    return
            else:
                yield scrapy.Request(
                        self.target_url+str(self.pageIndex),
                        callback=self.parseUserWeibo)
        else:
            return


    def filter_emoji(self,desstr):
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return co.sub("", desstr)
    # def start_requests(self):
    #     for url in self.start_urls:
    #         # yield scrapy.Request(url, cookies={'SUB=_2A253raVjDeRhGeNK7VAU9ibMyj-IHXVVUcsrrDV6PUJbkdAKLRHykW1NSTHSoRqOG_DS9sEmxXsav5R4qIkjW2JY; SUHB=0G0u6ey9_1-kHJ; SCF=AouotuoUWHGbf-lZy9F9XklNFHI2Cg02MgnGV5XKigVYq3AFp-Ypm7NdZI5Rkcx6N4BbeENGS9prGdXxn81MGBM.; SSOLoginState=1521079603; _T_WM=384bcb04b69ecf26cfa6fdb186fec5a3; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=featurecode%3D20000320%26luicode%3D20000174%26lfid%3Dhotword%26fid%3D1076032145291155%26uicode%3D10000011': 'true'})
    #         yield scrapy.Request(url, meta = {'cookiejar' : 1})