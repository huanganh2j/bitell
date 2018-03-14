# -*- coding: utf-8 -*-
import time
from selenium import webdriver

browser = webdriver.Chrome(executable_path="E:/toolsource/pythontoolsource/chromedriver.exe")
browser.get("https://weibo.com/")
time.sleep(10)
loginname = browser.find_element_by_id("loginname")
password = browser.find_elements_by_name("password");
submitBtn = browser.find_elements_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a')
loginname.send_keys("15874065601")
password[0].send_keys("923469an")
submitBtn[0].click()
print browser.page_source
