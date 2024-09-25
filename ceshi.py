import sqlite3
import os
from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import re
import   json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
page = ChromiumPage()
saveProse = page.ele('xpath://*[@id="root"]/div/div[1]/div/div[3]/div/div[1]/span[2]').text
print(saveProse)
while saveProse != '草稿已保存':
    page.wait(1)
    print('等待')
print(saveProse)
# page = ChromiumPage()
# lableLlist = {0: '自己输入文章链接', 1: '热点', 2: '娱乐', 3: '体育', 4: '军事', 5: '历史', 6: '财经'}
# navItem = lableLlist[1]
# scrollNum = 0
#
# page.get('https://www.toutiao.com/')
#
# page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul/li[9]/div[1]').click()
# page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[1]/div/ul').ele('text:{}'.format(navItem)).click()
# if scrollNum > 0:
#     for i in range(scrollNum):
#         page.scroll.to_bottom()
#         page.wait(1)
# dengdai = page.ele('@class=feed-m-top-refresh')
# page.wait.ele_hidden(dengdai)
# articleCard  = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]').children()
# print(articleCard)
# articleUrlList = []
# for i in range(len(articleCard)):
#     url = page.ele('xpath://*[@id="root"]/div/div[5]/div[1]/div/div/div/div[2]/div[{}]/div/div/a'.format(i+1)).link
#     articleUrlList.append(url)
# print(articleUrlList)

