import json
import sqlite3
import random
import base64
import os
import datetime
import time


def init():
    if (os.path.exists("./plugins/jrrp/database.db")):
        os.remove("./plugins/jrrp/database.db")
    con = sqlite3.connect("./plugins/jrrp/database.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE
  `jrrps` (
    `id` integer not null primary key autoincrement,
    `user_id` int null,
    `jrrp` int null,
    `last_date` int null
  )""")
    con.commit()
    cur.close()
    con.close()
    data = {'code': 200, 'info': "初始化成功"}
    data_json = json.dumps(data)
    return data_json


def update_jrrp(user, jrrp, last_date):
    con = sqlite3.connect("./plugins/jrrp/database.db")
    cur = con.cursor()

    sqlquery = "UPDATE jrrps SET jrrp = " + \
        str(jrrp)+", last_date="+str(last_date) + \
        " WHERE user_id = "+str(user['id'])

    cur.execute(sqlquery)

    con.commit()

    cur.close()
    con.close()
    return 1


def insert_jrrp(user, jrrp, last_date):
    con = sqlite3.connect("./plugins/jrrp/database.db")
    cur = con.cursor()

    sqlquery = "INSERT into `jrrps` (`user_id`, `jrrp`, `last_date`) values ('" + \
        str(user['id'])+"', "+str(jrrp)+", '"+str(last_date)+"')"

    cur.execute(sqlquery)

    con.commit()

    lower_id = cur.lastrowid

    cur.close()
    con.close()
    return 1


def check_user(user):
    isGetted = False
    con = sqlite3.connect("./plugins/jrrp/database.db")
    cur = con.cursor()
    result = cur.execute('SELECT * FROM jrrps WHERE user_id = ' +
                         str(user['id'])).fetchall()

    if (result):
        isGetted = True
    else:
        isGetted = False

    con.commit()
    cur.close()
    con.close()
    return isGetted


def rol(num: int, k: int, bits: int = 64):
    b1 = bin(num << k)[2:]
    if len(b1) <= bits:
        return int(b1, 2)
    return int(b1[-bits:], 2)


def get_hash(string: str):
    num = 5381
    num2 = len(string) - 1
    for i in range(num2 + 1):
        num = rol(num, 5) ^ num ^ ord(string[i])
    return num ^ 12218072394304324399


def get_jrrp_num(string: str):
    now = time.localtime()
    num = round(
        abs((get_hash("".join(
            ["asdfgbn",
             str(now.tm_yday), "12#3$45",
             str(now.tm_year), "IUY"])) / 3 + get_hash("".join(
                 ["QWERTY", string, "0*8&6",
                  str(now.tm_mday), "kjhg"])) / 3) / 527) % 1001)
    if num >= 970:
        num2 = 100
    else:
        num2 = round(num / 969 * 99)
    return num2


def get_jrrp(user):

    now = datetime.datetime.now()
    now = int(now.strftime("%Y%m%d"))
    if (check_user(user)):
        con = sqlite3.connect("./plugins/jrrp/database.db")
        cur = con.cursor()
        result = cur.execute('SELECT * FROM jrrps WHERE user_id = ' +
                             str(user['id'])).fetchall()
        print(result[0][3])
        if (result[0][3] < now):
            # rp_result = random.randint(1, 100)
            rp_result = get_jrrp_num(str(user['id']))
            update_jrrp(user, rp_result, now)
            data = {'code': 0, 'jrrp': rp_result}
            data_json = json.dumps(data)
            return data_json
        if (result[0][3] == now):
            data = {'code': 0, 'jrrp': result[0][2]}
            data_json = json.dumps(data)
            return data_json
        if (result[0][3] > now):
            data = {'code': 1}
            data_json = json.dumps(data)
            return data_json
    else:
        rp_result = random.randint(1, 100)
        insert_jrrp(user, rp_result, now)
        data = {'code': 0, 'jrrp': rp_result}
        data_json = json.dumps(data)
        return data_json
