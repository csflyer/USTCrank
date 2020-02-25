from . import main_view
from flask import render_template, flash, redirect, url_for
from .forms import LoginForm
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from ..models import User
from datetime import datetime
from functools import wraps

def TimeConsume():
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            start = datetime.now()
            print(func.__name__, 'start')
            result = func(*args, **kwargs)
            end = datetime.now()
            print(func.__name__, "运行耗时:", end-start)
            return result
        return wrap
    return decorator

@main_view.route('/', methods=['GET', 'POST'])
@TimeConsume()
def main():
    form = LoginForm()
    if (form.validate_on_submit()):
        user = User.query.get(form.kaohao.data)
        if user is not None:
            return render_template('score.html', user = user, major=user.major)
        post_url = 'http://yzb2.ustc.edu.cn/cjcx'
        post_data = {
            "ksbh" : form.kaohao.data,
            "zjhm" : form.id.data,
            "xm" : form.name.data,
            "code" : form.code.data
        }
        r = requests.post(post_url, data=post_data)
        if "未查询到相关记录" in r.text:
            flash("未查询到相关记录,请仔细检查或稍后再试")
            return redirect(url_for("main_view.main"))
        if "错误" in r.text:
            flash("验证码错误，请重新输入或稍后再试")
            return redirect(url_for("main_view.main"))
        if "result" not in r.text:
            flash("成绩抓取失败，请重新输入或稍后再试")
            return redirect(url_for("main_view.main"))
        user = User.insert_new(parse_html_data(r.text))
        if user is None:
            flash("数据插入失败，请联系管理员")
            return redirect(url_for("main_view.main"))
        return render_template('score.html', user=user, major=user.major)
    else:
        return render_template('form.html', form=form)


@TimeConsume()
def get_post_data(form):
    post_data = "zjhm=" + form.id.data + "&xm=" + quote(form.name.data) + "&code=" + form.code.data
    return post_data


# 从html爬取考生信息及分数
@TimeConsume()
def parse_html_data(html):
    bs = BeautifulSoup(html, 'html.parser')
    base_info = bs.select('.info-phone')[0].contents[1].contents[1].contents
    kaohao = base_info[7].contents[3].text
    temp_list = str.split(base_info[9].contents[3].text)
    college = temp_list[0]
    major = temp_list[1]
    subjects = bs.select('.result')[0].contents[1].contents[3].contents
    first_name = subjects[1].contents[1].text + subjects[1].contents[3].text
    first_score = int(subjects[1].contents[5].text)
    second_name = subjects[3].contents[1].text + subjects[3].contents[3].text
    second_score = int(subjects[3].contents[5].text)
    third_name = subjects[5].contents[1].text + subjects[5].contents[3].text
    third_score = int(subjects[5].contents[5].text)
    fourth_name = subjects[7].contents[1].text + subjects[7].contents[3].text
    fourth_score = int(subjects[7].contents[5].text)
    total_score = int(subjects[9].contents[3].text)
    return (kaohao, college, major, first_name, first_score, second_name, second_score, third_name, third_score
            , fourth_name, fourth_score, total_score)


@main_view.route('/captcha')
@TimeConsume()
def get_validate_image():
    url = 'http://yzb2.ustc.edu.cn/api/captcha'
    r = requests.get(url)
    return r.content


@main_view.route('/ranking_total_score/<college>/<major>')
@TimeConsume()
def total_ranking(college, major):
    start = datetime.now()
    users = User.query.filter_by(college=college, major=major).order_by(User.total_score.desc()).all()
    end = datetime.now()
    print("查询" + str(len(users)) + "条数据用时:", end - start)
    return render_template("ranking.html", users=users, head='按总分排名')


@main_view.route('/ranking_net_score/<college>/<major>')
@TimeConsume()
def net_ranking(college, major):
    start = datetime.now()
    users = User.query.filter_by(college=college, major=major).order_by(User.net_score.desc()).all()
    end = datetime.now()
    print("查询" + str(len(users)) + "条数据用时:", end - start)
    return render_template("ranking.html", users=users, head='除去政治后成绩排名')
