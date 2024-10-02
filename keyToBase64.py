import base64
import datetime

def baseKey(data,type):
    data = data.encode('utf-8')
    if type == 'encode':
        res = base64.b64encode(data).decode()
        return  res
    elif type == 'decode':
        res = base64.b64decode(data).decode()
        return res
 
nowTime = datetime.datetime.now()
etime =( nowTime.replace(year = nowTime.year+1)).strftime('%Y-%m-%d %H:%M:%S')
ctime = nowTime.strftime('%Y-%m-%d %H:%M:%S')

keyBase64 ={
    'host':'WIN-20241001IPM',
    'cdk':'LzR6FqP2lGpOqknf',
    'ctime':etime,
    'etime':ctime,
}

host='XTZJ-20240924UO'
cdk='A8rjimA6ZXTZxVdn'

for i in range(3):
    cdk = baseKey(cdk,'encode')
print( 'cdk:'+cdk)
for i in range(3):
    host = baseKey(host,'encode')
print('host:' + host)
for i in range(3):
    etime = baseKey(etime,'encode')
print('ctime:'+  etime)
for i in range(3):
    ctime = baseKey(ctime,'encode')
print('etime:'+ ctime)