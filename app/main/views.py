from . import main_view
from flask import render_template, flash, redirect, url_for, request, current_app, make_response
from flask_login import login_user, logout_user, current_user
from .forms import CJCXForm, LoginForm, ResetPasswordForm, SimpleResetPwForm
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
from ..models import User
from datetime import datetime
from functools import wraps

# 装饰器 用于调试 显示调用每个函数耗费时间
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

# 装饰器 用于要登录才能访问的页面
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("要访问此页面，请先登录")
            return redirect(url_for("main_view.login"))
        else:
            r = func(*args, **kwargs)
            return r
    return wrap

# 退出登录
@main_view.route("/logout")
def logout():
    if current_user.is_authenticated:
        flash("已安全退出登录", category="info")
        logout_user()
    return redirect(url_for("main_view.login"))

# 登录
@main_view.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.kaohao.data)
        if user is None or not user.validate_password(form.password.data):
            flash("准考证号或密码错误!")
            return redirect(url_for("main_view.login"))
        login_user(user)
        return redirect(url_for("main_view.score"))
    else:
        return render_template("form.html", form=form)

# 修改密码
@main_view.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        form = SimpleResetPwForm()
    else:
        form = ResetPasswordForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if current_user.change_password(form.password.data) is not None:
                flash("修改密码成功", category="info")
            else:
                flash("修改密码失败, 请联系管理员")
            logout_user()
            return redirect(url_for("main_view.login"))
        r = scrawl_score(form)
        if not isinstance(r, requests.Response):
            flash(r)
            return redirect(url_for("main_view.reset_password"))
        user = User.query.get(form.kaohao.data)
        user = user.change_password(form.password.data)
        if user is None:
            flash("查询密码更改失败，请联系管理员")
        else:
            flash("修改密码成功", category="info")
        logout_user()
        return redirect(url_for("main_view.login"))
    return render_template("form.html", form=form)

# 处理成绩查询请求
@main_view.route('/cjcx', methods=['GET', 'POST'])
def cjcx():
    if current_user.is_authenticated:
        return redirect(url_for("main_view.score"))
    form = CJCXForm()
    if form.validate_on_submit():
        user = User.query.get(form.kaohao.data)
        if user is not None:
            flash("此准考证号已查过成绩，请直接登陆")
            return redirect(url_for("main_view.login"))
        r = scrawl_score(form)
        if not isinstance(r, requests.Response):
            flash(r)
            return redirect(url_for("main_view.cjcx"))
        user = User.insert_new(parse_html_data(r.text), password=form.password.data)
        if user is None:
            flash("数据插入失败，请联系管理员")
            return redirect(url_for("main_view.cjcx"))
        login_user(user)
        return redirect(url_for("main_view.score"))
    else:
        return render_template('form.html', form=form)

# 从 USTC网站上查询成绩
def scrawl_score(form):
    post_url = 'http://yzb2.ustc.edu.cn/cjcx'
    post_data = {
        "ksbh": form.kaohao.data,
        "zjhm": form.id.data,
        "xm": form.name.data,
        "code": form.code.data
    }
    r = requests.post(post_url, data=post_data)
    if "未查询到相关记录" in r.text:
        return "未查询到相关记录,请仔细检查或稍后再试"
    if "错误" in r.text:
        return "验证码错误，请重新输入或稍后再试"
    if "result" not in r.text:
        return "成绩抓取失败，请重新输入或稍后再试"
    return r


# 显示分数信息
@main_view.route("/score")
@login_required
def score():
    return render_template('score.html')


# 从html爬取考生信息及分数
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


# 从官网的 api 获取验证码并返回
@main_view.route('/captcha')
def get_validate_image():
    url = 'http://yzb2.ustc.edu.cn/api/captcha'
    r = requests.get(url)
    response = make_response(r.content)
    response.headers['Content-Type'] = 'image/jpg'
    return response


# 按总分排名
@main_view.route('/ranking_total/<college>/<major>')
@login_required
def ranking_total(college, major):
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(college=college, major=major).order_by(User.total_score.desc()).paginate(
        page, per_page=current_app.config["USERS_PER_PAGE"], error_out=False
    )
    users = pagination.items
    return render_template("ranking.html", users=users, pagination=pagination,
                           head='按总分排名', is_total_ranking=True,
                           USERS_PER_PAGE=current_app.config["USERS_PER_PAGE"], title="排名查询")


# 按除政治后总分排名
@main_view.route('/ranking_net/<college>/<major>')
@login_required
def ranking_net(college, major):
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter_by(college=college, major=major).order_by(User.net_score.desc()).paginate(
        page, per_page=current_app.config["USERS_PER_PAGE"], error_out=False
    )
    users = pagination.items
    return render_template("ranking.html", users=users, pagination=pagination,
                           head='除去政治后成绩排名', is_total_ranking=False,
                           USERS_PER_PAGE=current_app.config["USERS_PER_PAGE"], title="排名查询")