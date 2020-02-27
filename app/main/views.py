from . import main_view
from flask import render_template, flash, redirect, url_for, request, current_app
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
        start = datetime.now()
        user = User.query.get(form.kaohao.data)
        end = datetime.now()
        print("查询单个数据用时:", end - start)
        if user is not None:
            return redirect(url_for("main_view.score", kaohao=user.kaohao))
        post_url = 'http://yzb2.ustc.edu.cn/cjcx'
        post_data = {
            "ksbh" : form.kaohao.data,
            "zjhm" : form.id.data,
            "xm" : form.name.data,
            "code" : form.code.data
        }
        start = datetime.now()
        r = requests.post(post_url, data=post_data)
        end = datetime.now()
        print("抓取成绩耗时:", end - start)
        if "未查询到相关记录" in r.text:
            flash("未查询到相关记录,请仔细检查或稍后再试")
            return redirect(url_for("main_view.main"))
        if "错误" in r.text:
            flash("验证码错误，请重新输入或稍后再试")
            return redirect(url_for("main_view.main"))
        if "result" not in r.text:
            flash("成绩抓取失败，请重新输入或稍后再试")
            return redirect(url_for("main_view.main"))
        start = datetime.now()
        user = User.insert_new(parse_html_data(r.text))
        end = datetime.now()
        print("插入数据耗时:", end - start)
        if user is None:
            flash("数据插入失败，请联系管理员")
            return redirect(url_for("main_view.main"))
        return redirect(url_for("main_view.score", kaohao=user.kaohao))
    else:
        return render_template('form.html', form=form)


@main_view.route("/score/<kaohao>")
@TimeConsume()
def score(kaohao):
    user = User.query.get(kaohao)
    if user is None:
        flash("无此记录，请检查准考证号")
        return redirect(url_for("main_view.main"))
    else:
        return render_template('score.html', user=user, major=user.major)


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
    start = datetime.now()
    r = requests.get(url)
    end = datetime.now()
    print("获取图片耗时:", end - start)
    return r.content


@main_view.route('/ranking_total_score/<college>/<major>')
@TimeConsume()
def total_ranking(college, major):
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(college=college, major=major).order_by(User.total_score.desc()).paginate(
        page, per_page=current_app.config["USERS_PER_PAGE"], error_out=False
    )
    users = pagination.items
    return render_template("ranking.html", users=users, pagination=pagination,
                           head='按总分排名', is_total_ranking=True,
                           USERS_PER_PAGE=current_app.config["USERS_PER_PAGE"])


@main_view.route('/ranking_net_score/<college>/<major>')
@TimeConsume()
def net_ranking(college, major):
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(college=college, major=major).order_by(User.net_score.desc()).paginate(
        page, per_page=current_app.config["USERS_PER_PAGE"], error_out=False
    )
    users = pagination.items
    return render_template("ranking.html", users=users, pagination=pagination,
                           head='除去政治后成绩排名', is_total_ranking=False,
                           USERS_PER_PAGE=current_app.config["USERS_PER_PAGE"])