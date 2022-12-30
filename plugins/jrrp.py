import json
import sqlite3
import random
import base64
import os
import datetime
import time


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
    num = round(abs((get_hash("".join([
        "asdfgbn",
        str(now.tm_yday),
        "12#3$45",
        str(now.tm_year),
        "IUY"
    ])) / 3 + get_hash("".join([
        "QWERTY",
        string,
        "0*8&6",
        str(now.tm_mday),
        "kjhg"
    ])) / 3) / 527) % 1001)
    if num >= 970:
        num2 = 100
    else:
        num2 = round(num / 969 * 99)
    return num2


def get_msg(jrrp):
    msg = '...'
    if (jrrp == 100):
        msg = "100！100！100！！！！！"
    if (jrrp >= 90 and jrrp < 100):
        msg = str(jrrp)+"！好评如潮！"
    if (jrrp >= 60 and jrrp < 90):
        msg = str(jrrp)+"！是不错的一天呢！"
    if (jrrp > 50 and jrrp < 60):
        msg = str(jrrp)+"！还行啦还行啦。"
    if (jrrp == 50):
        msg = str(jrrp)+"！五五开……"
    if (jrrp >= 40 and jrrp < 50):
        msg = str(jrrp)+"！还……还行吧……？"
    if (jrrp >= 11 and jrrp < 40):
        msg = str(jrrp)+"！呜哇……"
    if (jrrp >= 0 and jrrp < 11):
        msg = str(jrrp)+"！……（没错，是百分制）"
    return msg


def get_jrrp(user):

    now = datetime.datetime.now()
    now = int(now.strftime("%Y%m%d"))
    rp_result = get_jrrp_num(str(user['id']))
    data = {'code': 0, 'jrrp': rp_result, 'msg': get_msg(rp_result)}
    data_json = json.dumps(data)
    return data_json
