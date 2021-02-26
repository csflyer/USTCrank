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
    # anti-csrf form
    app.config['SECRET_KEY'] = 'USTC'
    # num of items in the ranking page
    app.config['USERS_PER_PAGE'] = 100

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    from .main import main_view
    app.register_blueprint(main_view)

    return app

