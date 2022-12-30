import os
import cqhttp_py
import json
import yaml
from flask import Flask, request

from plugins import cave, jrrp

config = 'Null'


with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

owner_id = config['user']['owner']

app = Flask(__name__)

cqhttp_py.port = config['cqhttp_py']['port']

cqhttp_py.host = config['cqhttp_py']['host']


@app.route('/', methods=["POST"])
def post_data():
    global owner_id
    rawjson = request.get_data()

    rawjson = json.loads(rawjson)
    print(rawjson)
    if rawjson['post_type'] == 'meta_event':
        print('接收到心跳')
    if rawjson['post_type'] == 'message':
        if rawjson['message_type'] == 'private':

            user_nick = rawjson['sender']['nickname']
            user_id = rawjson['sender']['user_id']
            user_type = rawjson['sub_type']
            msg_id = rawjson['message_id']
            msg_text = rawjson['raw_message']
            print("收到 "+user_nick+"("+str(user_id)+") 的消息："+msg_text)
            if (user_id == 2310933302 and msg_text == '.init_cave'):
                cave.init()
                cqhttp_py.send_private_msg(
                    2310933302, "已重置回声洞数据库")
            if (user_id == 2310933302 and msg_text == '.init_jrrp'):
                jrrp.init()
                cqhttp_py.send_private_msg(
                    2310933302, "已重置人品数据库")

        if rawjson['message_type'] == 'group':
            user_nick = rawjson['sender']['nickname']
            user_id = rawjson['sender']['user_id']
            user = {
                'nickname': rawjson['sender']['nickname'], 'id': rawjson['sender']['user_id']}
            msg = {'id': rawjson['message_id'], 'text': rawjson['raw_message'], 'lengh': len(
                rawjson['raw_message'])}

            group_id = rawjson['group_id']
            print("收到 群"+str(group_id)+" 成员 "+user['nickname'] +
                  "("+str(user['id'])+") 的消息："+msg['text'])
            if (msg['text'][0] == '。' or msg['text'][0] == '.'):
                print('Command Get')
                if (msg['text'][1:6] != "cave-" and (msg['text'][1:5] == 'cave' or msg['text'][1:5] == 'cave')):
                    print(user['nickname'] +
                          "("+str(user['id'])+") 尝试获取一条回声洞")
                    rawcave = json.loads(cave.get_random_cave())
                    send_msg = """回声洞 —— ("""+str(rawcave['id'])+""")

"""+rawcave['cave']+"""
—— """+rawcave['user_name']

                    cqhttp_py.send_group_msg(group_id, send_msg)
                    return "{\"code\" : 0}"
                if (msg['text'][1:6] == "cave-"):
                    if (msg['text'][1:7] == 'cave-a'):
                        error_msg = {
                            'nothing_get': '请提供回声洞内容', 'error_command': "命令错误！\n命令格式: .cave-a XXXX(回声洞内容)"}
                        if (len(msg['text']) == 7):
                            cqhttp_py.send_group_msg(
                                group_id, error_msg["nothing_get"])
                            return "{\"code\" : 1,\"error\" = True}"
                        if (msg['text'][7] != ' '):
                            cqhttp_py.send_group_msg(
                                group_id, error_msg["error_command"])
                            return "{\"code\" : 1,\"error\" = True}"
                        user_cave = msg['text'][8:msg['lengh']]
                        return_data = json.loads(
                            cave.add_cave(user, user_cave))
                        send_msg = "[CQ:at,qq="+str(user['id']) + \
                            "] 已添加，序号为 "+str(return_data['id'])
                        cqhttp_py.send_group_msg(group_id, send_msg)

                    if (msg['text'][1:7] == 'cave-r'):
                        error_msg = {
                            'nothing_get': '请提供回声洞ID', 'error_command': "命令错误！\n命令格式: .cave-r ID"}
                        if (len(msg['text']) == 7):
                            cqhttp_py.send_group_msg(
                                group_id, error_msg["nothing_get"])
                            return "{\"code\" : 1,\"error\" = True}"
                        if (msg['text'][7] != ' '):
                            cqhttp_py.send_group_msg(
                                group_id, error_msg["error_command"])
                            return "{\"code\" : 1,\"error\" = True}"
                        cave_id = msg['text'][8:msg['lengh']]
                        return_data = json.loads(
                            cave.remove_cave(cave_id))
                        print(return_data)

                        send_msg = "[CQ:at,qq="+str(user['id']) + \
                            "] 移除回声洞 —— ("+str(return_data['raw_info']['id'])+""")

"""+return_data['raw_info']['cave']+"""
—— """+return_data['raw_info']['user_name']
                        cqhttp_py.send_group_msg(group_id, send_msg)
                if (msg['text'][1:msg['lengh']] == 'jrrp'):
                    return_data = json.loads(jrrp.get_jrrp(user))
                    if (return_data['code'] == 1):
                        year = str(int(return_data['until_date'] / 10000))
                        month = str(
                            int(int(return_data['until_date'] % 10000)/100))
                        day = str(int(return_data['until_date'] % 100))
                        send_msg = "[CQ:at,qq="+str(user['id']) + \
                            "]Ops! 看起来你穿越了时空，也有可能是兔兔的问题！\n无论如何，你下一次找兔兔占卜的时间是:\n" + \
                            year+"."+month+"."+day+" \n兔兔始终欢迎你的光临!"
                        cqhttp_py.send_group_msg(group_id, send_msg)
                    if (return_data['code'] == 0):
                        send_msg = "[CQ:at,qq="+str(user['id']) + \
                            "] 你今天的人品值是："+return_data['msg']
                        cqhttp_py.send_group_msg(group_id, send_msg)
    return "OK"


@app.route('/class/')
def get_class():
    print("Yes!")
    return "OK"


'''
message_type 是消息类型群聊或私聊 uid 是qq号 gid 是群号默认为空
'''
if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=int(config['POST']['port']))
