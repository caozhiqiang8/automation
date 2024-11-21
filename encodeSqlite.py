import sqlite3
 
# 引入SQLCipher驱动
sqlite3.register_dll('sqlcipher')
 
# 创建一个加密的SQLite数据库
conn = sqlite3.connect('automation.db')
cursor = conn.cursor()
 
# 加密数据库，设置密钥
cursor.execute('PRAGMA key = "123456";')
 
# 现在可以正常使用数据库，加密会自动应用于所有数据
cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT);')
cursor.execute('INSERT INTO test (value) VALUES ("example");')
 
conn.commit()
conn.close()