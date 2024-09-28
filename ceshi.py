import sqlite3
import os
from DrissionPage import ChromiumPage
from DrissionPage.common import Actions,Keys
import re
import   json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64

def baseKey(data,type):
    data = data.encode('utf-8')
    if type == 'encode':
        res = base64.b64encode(data).decode()
        return  res
    elif type == 'decode':
        res = base64.b64decode(data).decode()
        return res

data = 'caozhiqiangdeMacBook-Pro.local'

for i  in range(3):
    data = baseKey(data=data,type='encode')
print(data)


# ddata = baseKey(data=edata,type='decode')
# print(ddata)