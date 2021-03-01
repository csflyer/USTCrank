import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy(use_native_unicode='utf-8')
bootstrap =  Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main_view.main'


def create_app():
    app = Flask(__name__)
    # 数据库地址
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/USTCrank/scores.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
    # 表单 防CSRF & password hash
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    if app.config['SECRET_KEY'] is None:
        raise ValueError(" you must set environment variable SECRET_KEY and remember it before it runs"
                         "(don't change it after that)")
    # 排名每页显示人数
    app.config['USERS_PER_PAGE'] = 100

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    from .main import main_view
    app.register_blueprint(main_view)

    return app

