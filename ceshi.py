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
print('''
[0]自己输入文章链接 [1]热点 [2]娱乐 [3]体育 [4]军事 [5]历史 [6]财经
''')
inputLable = int(input('请选择需要采集的文章领域(输入数字,如果不输入默认热点)：'))
