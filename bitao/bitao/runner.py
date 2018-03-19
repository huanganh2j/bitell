#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import time


def doSth():
    # 把爬虫程序放在这个类里
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(u'这个程序要开始疯狂的运转啦')


# 一般网站都是1:00点更新数据，所以每天凌晨一点启动
def main(h=1, m=0):
    while True:
        while True:
            now = datetime.datetime.now()
            # print(now.hour, now.minute)
            # if now.hour == h and now.minute == m:
            if now.second == 0:
                break
                # 每隔60秒检测一次
            time.sleep(2)
        doSth()
main()