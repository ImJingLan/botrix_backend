'''
 Copyright ImJingLan 2021

 Dev Time:2021\07\27

 Version:Alpha 0.0.6
'''
import requests
import re
import ctypes
import sys

host = '127.0.0.1'
port = 5700

if __name__ == '__main__':
    print(" * Please import this file into your qqrobot python programe\n * You can find Doc here:https://github.com/ImJingLan/cqhttp_py")

if __name__ != '__main__':

    print(" * Thanks for install cqhttp_py lib!\n * You can find Doc here:https://github.com/ImJingLan/cqhttp_py\n")


def send_private_msg(user_id, msg, auto_escape=False):
    data = {
        'user_id': user_id,
        'message': msg,
        'auto_escape': auto_escape
    }
    return requests.post('http://'+host+':'+str(port)+'/send_private_msg', data=data).text


def send_group_msg(group_id, msg, auto_escape=False):
    data = {
        'group_id': group_id,
        'message': msg,
        'auto_escape': auto_escape
    }
    return requests.post('http://'+host+':'+str(port)+'/send_group_msg', data=data).text


def delete_msg(message_id):
    data = {
        'message_id': message_id
    }
    requests.post('http://'+host+':'+str(port)+'/delete_msg', data=data)


def get_msg(message_id):
    data = {
        'message_id': message_id
    }
    return requests.post('http://'+host+':'+str(port)+'/get_msg', data=data).text


def set_group_kick(group_id, user_id, reject_add_request=False):
    data = {
        'group_id': group_id,
        'user_id': user_id,
        'reject_add_request': reject_add_request
    }
    return requests.post('http://'+host+':'+str(port)+'/set_group_kick', data=data).text


def set_group_whole_ban(group_id, enable=True):
    data = {
        'group_id': group_id,
        'enable': enable,
    }
    return requests.post('http://'+host+':'+str(port)+'/set_group_whole_ban', data=data).text


def set_group_leave(group_id, is_dismiss=False):
    data = {
        'group_id': group_id,
        'is_dismiss': is_dismiss,
    }
    return requests.post('http://'+host+':'+str(port)+'/set_group_leave', data=data).text
