import re
from DrissionPage import ChromiumOptions, ChromiumPage

with open('config.txt', 'r', encoding='UTF-8-sig') as file:
        fileLines = file.readlines()           
config = {}
for i in fileLines:
    key, value = i.strip().split('：')
    config[key] = value
if 'dataPath' in config:
        dataPath = config['dataPath']
if 'localPort' in config:
    localPort = config['localPort']
    localPort = re.split(',',localPort) 

if len(localPort)>1:

    for i in range(len(localPort)+1):
        if i == 0:
            page = ChromiumPage()
        else:
            do = ChromiumOptions().set_paths(local_port=int(localPort[i-1]), user_data_path='{}:\\userData\\userData_{}'.format(dataPath,int(localPort[i-1])))
            page = ChromiumPage(addr_or_opts=do)
else:
    page = ChromiumPage()