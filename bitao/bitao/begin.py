import subprocess

import schedule
import time
from scrapy import cmdline


def do_work():
    subprocess.Popen('scrapy crawl jinse ')
    # print 'you job start ......'
    # cmdline.execute("scrapy crawl jinse".split())
# cmdline.execute("scrapy crawl weibosecond".split())
# cmdline.execute("scrapy runspider C:/Users/huangan/PycharmProjects/bitell/bitao/bitao/spiders/weibosecondspider.py".split())
if __name__ == '__main__':
    schedule.every(3).minutes.do(do_work)
    while True:
        schedule.run_pending()
        time.sleep(1)
