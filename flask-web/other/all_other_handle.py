# coding=utf-8
from flask import session

from db import MysqlInfo

handle_db = MysqlInfo()


# 判断输入的是否合格
class JudgeLogin:
    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type
        count = 0
        for flag in handle_db.login(self.username, self.password):
            count += 1
            print flag
        if count != 0:
            return True
        else:
            return False

    def j_username(self):
        if len(self.username) < 2:
            msg = '用户名长度不够！'
            return msg
        if len(self.username) > 10:
            msg = '用户名超长！'
            return msg

    def j_password(self):
        if len(self.password) < 6:
            msg = '密码长度不够！'
            return msg
        if len(self.password) > 16:
            msg = '密码超长了！'
            return msg

    def j_usertype(self):
        if self.user_type not in [1, 2, 3]:
            return False
        else:
            return True


def judge_user_type(username):
    usertype = handle_db.user_type(username)
    if usertype == 1:
        url = 'doc'
    elif usertype == 2:
        url = 'user'
    elif usertype == 3:
        url = 'lab'
    else:
        url = 'login'
    return url