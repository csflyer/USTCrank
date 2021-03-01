from . import db
from flask import current_app
from sqlalchemy.exc import IntegrityError
from . import login_manager
from hashlib import md5


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# ORM 数据类
class User(db.Model):
    __tablename__ = 'user'

    kaohao = db.Column(db.String(18), unique=True, primary_key=True)
    password = db.Column(db.String(20))
    college = db.Column(db.String(32), index=True)
    major = db.Column(db.String(64), index=True)
    subject1_code = db.Column(db.String(64))
    subject1_score = db.Column(db.INTEGER)
    subject2_code = db.Column(db.String(64))
    subject2_score = db.Column(db.INTEGER)
    subject3_code = db.Column(db.String(64))
    subject3_score = db.Column(db.INTEGER)
    subject4_code = db.Column(db.String(64))

    subject4_score = db.Column(db.INTEGER)
    net_score = db.Column(db.INTEGER, index=True)
    total_score = db.Column(db.INTEGER, index=True)

    def get_id(self):
        return self.kaohao

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def change_password(self, password):
        temp_password = User.hash_password(password)
        if temp_password == self.password:
            return self
        self.password = temp_password
        db.session.add(self)
        try:
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            return None
    
    def validate_password(self, password):
        return self.password == self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return md5((current_app.config['SECRET_KEY'] + password).encode(encoding='UTF-8')).hexdigest()

    @staticmethod
    def insert_new(info_list, password):
        (kaohao, college, major, first_name, first_score, second_name, second_score, third_name, third_score
         , fourth_name, fourth_score, total_score) = info_list
        user =  User(kaohao=kaohao,
                     password=User.hash_password(password),
                    college = college,
                    major=major,
                    subject1_code = first_name,
                    subject1_score = first_score,
                    subject2_code = second_name,
                    subject2_score = second_score,
                    subject3_code = third_name,
                    subject3_score = third_score,
                    subject4_code = fourth_name,
                    subject4_score = fourth_score,
                    net_score= second_score + third_score + fourth_score,
                    total_score = total_score)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            return None
