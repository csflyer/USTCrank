import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

db = MongoEngine()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main_view.main'


def create_app():
    app = Flask(__name__)
    # mongo db setting
    app.config['MONGODB_SETTINGS'] = {
        'db': 'users',
        'host': '127.0.0.1',
        'port': 27017
    }
    # anti-csrf form and password hash
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    if app.config['SECRET_KEY'] is None:
        raise ValueError(" you must set environment variable SECRET_KEY and remember it before it runs"
                         "(don't change it after that)")
    # num of items in the ranking page
    app.config['USERS_PER_PAGE'] = 100

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    from .main import main_view
    app.register_blueprint(main_view)

    return app

