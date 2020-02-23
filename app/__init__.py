from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(use_native_unicode='utf-8')
bootstrap =  Bootstrap()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///d:/temp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
    app.config['SECRET_KEY'] = 'USTC'

    db.init_app(app)
    bootstrap.init_app(app)

    from .main import main_view
    app.register_blueprint(main_view)

    return app

