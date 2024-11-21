import re
from DrissionPage import ChromiumOptions, ChromiumPage

with open('config.txt', 'r', encoding='UTF-8-sig') as file:
        fileLines = file.readlines()           
config = {}
for i in fileLines:
    key, value = i.strip().split('：')
    config[key] = value
if '磁盘' in config:
        dataPath = config['磁盘']
if '多开' in config:
    localPort = config['多开']
    localPort = re.split(',',localPort) 

if len(localPort)>0:
    for i in range(len(localPort)+1):
        if i == 0:
            do = ChromiumOptions().set_paths(local_port=9222, user_data_path='{}:\\userData\\userData_{}'.format(dataPath,9222))
            page = ChromiumPage(addr_or_opts=do)
        else:
            do = ChromiumOptions().set_paths(local_port=int(localPort[i-1]), user_data_path='{}:\\userData\\userData_{}'.format(dataPath,int(localPort[i-1])))
            page = ChromiumPage(addr_or_opts=do)
else:
    page = ChromiumPage()