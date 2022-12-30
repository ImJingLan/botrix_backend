import json
import sqlite3
from random import randint
import base64
import os


def get_random_cave():
    con = sqlite3.connect("./plugins/cave/database.db")
    cur = con.cursor()
    result = cur.execute(
        'SELECT * FROM caves order by random() limit 1').fetchall()
    id = result[0][0]
    user_name = result[0][1]
    user_id = result[0][2]
    cave = result[0][3]
    con.commit()
    cur.close()
    con.close()
    data = {'id': id, 'user_name': user_name,
            'user_id': user_id, 'cave': cave}
    data_json = json.dumps(data)
    return data_json


def get_cave(id):
    con = sqlite3.connect("./plugins/cave/database.db")
    cur = con.cursor()
    result = cur.execute(
        'SELECT * FROM caves WHERE id = '+str(id)).fetchall()
    id = result[0][0]
    user_name = result[0][1]
    user_id = result[0][2]
    cave = result[0][3]
    con.commit()
    cur.close()
    con.close()
    data = {'id': id, 'user_name': user_name,
            'user_id': user_id, 'cave': cave}
    data_json = json.dumps(data)
    return data_json


def add_cave(user, cave):
    con = sqlite3.connect("./plugins/cave/database.db")
    cur = con.cursor()

    sqlquery = "INSERT into `caves` (`user_name`, `user_id`, `cave`) values ('" + \
        user['nickname']+"', "+str(user['id'])+", '"+cave+"')"

    cur.execute(sqlquery)

    con.commit()

    lower_id = cur.lastrowid

    cur.close()
    con.close()
    data = {'id': lower_id,
            'user_name': user['nickname'], 'user_id': user['id'], 'cave': cave}
    data_json = json.dumps(data)
    return data_json


def remove_cave(id):

    raw_info = json.loads(get_cave(id))

    con = sqlite3.connect("./plugins/cave/database.db")
    cur = con.cursor()

    sqlquery = "DELETE FROM `caves` WHERE id = "+str(id)+""

    cur.execute(sqlquery)

    con.commit()

    cur.close()
    con.close()
    data = {'removed': 1, 'id': id, "raw_info": raw_info}
    data_json = json.dumps(data)
    return data_json


def init():
    if (os.path.exists("./plugins/cave/database.db")):
        os.remove("./plugins/cave/database.db")
    con = sqlite3.connect("./plugins/cave/database.db")
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE
  `caves` (
    `id` integer not null primary key autoincrement,
    `user_name` varchar(255) null,
    `user_id` int null,
    `cave` varchar(255) null
  )""")
    con.commit()
    cur.close()
    con.close()
    data = {'code': 200, 'info': "初始化成功"}
    data_json = json.dumps(data)
    return data_json
