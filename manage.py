from app.models import User
from app import create_app, db
from flask_script import Manager, Shell
from werkzeug.exceptions import InternalServerError
from prettytable import PrettyTable
import csv

app = create_app()
manager = Manager(app)


# 处理 500 内部错误，用于调试
@app.errorhandler(InternalServerError)
def internal_server_error(e):
    print(e.code)
    print(e.name)
    print(e.description)
    return "Internal Server Error"


# 创建围观账户
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


# 查看后台是否有重复考号
def print_dup():
    s = set()
    for user in User.objects:
        if user.kaohao in s:
            print(user.kaohao)
        else:
            s.add(user.kaohao)


# 统计数据库内数据条数
def print_len():
    print("数据库总记录数: ", len(User.objects), "\n")


# 统计各学院各专业报考人数
def print_statistics():
    print_len()

    map = {}

    for user in User.objects:
        # 跳过围观账户
        if user.total_score == 0:
            continue
        if user.college in map:
            v = map[user.college]
            v[0] += 1
            if user.major in v[1]:
                v[1][user.major] += 1
            else:
                v[1][user.major] = 1
        else:
            map[user.college] = [1, {user.major: 1}]

    table = PrettyTable()
    table.field_names = ["学院", "学院总人数", "专业", "专业总人数"]

    for college, v in map.items():
        clg_name_printed = False
        for major, num in v[1].items():
            if not clg_name_printed:
                table.add_row([college, v[0], major, num])
                clg_name_printed = True
            else:
                table.add_row(["", "", major, num])

    print(table)


# 导出数据到到csv文件
def export():
    with open("./scores.csv", "w", encoding="utf-8-sig", newline="") as file:
        header = ["koahao", "college", "major", "subject1", "subject1_score", "subject2", "subject2_score",
                    "subject3", "subject3_score", "subject4", "subject4_score", "net_score", "total_score"]
        writer = csv.DictWriter(file, header)
        writer.writeheader()
        rows = [{"koahao" : user.kaohao,
                "college": user.college,
                "major": user.major,
                "subject1": user.subject1_code,
                "subject1_score": user.subject1_score,
                "subject2": user.subject2_code,
                "subject2_score": user.subject2_score,
                "subject3": user.subject3_code,
                "subject3_score": user.subject3_score,
                "subject4": user.subject4_code,
                "subject4_score": user.subject4_score,
                "net_score": user.net_score,
                "total_score": user.total_score} for user in User.objects]
        writer.writerows(rows)


def make_shell_context():
    return dict(app=app, db=db, User=User, create_super_user=create_super_user, print_len=print_len,
                    print_dup=print_dup, print_sta=print_statistics)


@manager.command
def run():
    app.run(port=80)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()