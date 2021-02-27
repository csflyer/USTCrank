import os
from app.models import User
from app import create_app, db
from flask_script import Manager, Shell
from werkzeug.exceptions import InternalServerError


app = create_app()
manager = Manager(app)


# 处理 500 内部错误，用于调试
@app.errorhandler(InternalServerError)
def internal_server_error(e):
    print(e.code)
    print(e.name)
    print(e.description)
    return "Internal Server Error"


def create_super_user(kaohao, pwd):
    if len(kaohao) != 15:
        print("考号必须为15位")
    if len(pwd) != 6:
        print("密码必须为6位")

    if User.get(kaohao) is not None:
        print("该考号已存在，请换个再试")
    User.insert_new((kaohao, "225软件学院", "085400电子信息",
                     "101思想政治理论", 0, "204英语二", 0,
                     "302数学二", 0, "408计算机学科专业基础综合", 0,
                     0), pwd)


def make_shell_context():
    return dict(app=app, db=db, User=User, create_super_user=create_super_user)


@manager.command
def run():
    app.run(port=80)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()