import sqlite3
import os

#
# file_path = os.getcwd()
# hostname = os.popen('hostname').read().strip()
#
# conn = sqlite3.connect('automation.db')
# cursor = conn.cursor()
# sql = '''
# select * from host_key where  host='{}' and key != ''
# '''.format(hostname)
#
# result = cursor.execute(sql).fetchall()
#
# cursor.close()
# conn.close()
#
# print(result)
# if  result  :
#     print('有数据')
# else:
#     print("不存在")
#
with open(r'文章链接.txt', 'r', encoding='utf-8') as file:
    cdk = file.read()

print(cdk)
urlList = cdk.splitlines()
print(urlList)