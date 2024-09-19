import sqlite3
import os
from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import re

# page = ChromiumPage()
# url = 'https://a.mp.uc.cn/article.html?uc_param_str=frdnsnpfvecpntnwprdssskt&wm_aid=630a5e57226e49b0b5c60ec8fdd09517'
# page.get(url)
# connect = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/div[2]').text
# title = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/h1').text
# img = page.ele('xpath://*[@id="react_app_content_id"]/div[3]/div[2]').eles('tag:img')
# imgList = img.get.links()
# print(title)
# print(connect)
# print(imgList)

# page.get(url)
# connect = page.ele('xpath://*[@id="react_app_content_id"]/div/div[4]/div[2]/p[1]').text
# title = connect[:30]
# imgFather = page.ele('xpath://*[@id="gridContainer"]').children()
# imgList = []
# for i in imgFather:
#     img = i.child().child().attr('style')
#     print(img)
#     zhengze = r'"([^"]*)"|'r'\'([^\']*)\''
#     imgZhengZe = [m[0] for m in (re.findall(zhengze, img)) if m[0]]
#     imgList.append(imgZhengZe[0])


result = '(相似度:23.4%)'
result = float(result[5:-2])
print(result)
if result < 25.00:
    print('通过')
else:
    print('不通过')