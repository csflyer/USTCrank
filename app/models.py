from . import db
from flask import current_app
from flask_mongoengine import BaseQuerySet
from . import login_manager
from hashlib import md5


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# 自定义的查询方式，用于输出排名与分页
class CustomQuerySet(BaseQuerySet):

    def get_ranking(self, college, major, subject1, subject2, subject3, subject4, order_field, page, per_page):
        return self.filter(college=college, major=major, subject1_code=subject1, subject2_code=subject2,
                           subject3_code=subject3, subject4_code=subject4).order_by("-" + order_field).paginate(
            page=page, per_page=per_page)


# ORM 数据类
class User(db.Document):
    __tablename__ = 'users'
    # 注册上面自定义的查询方式
    meta = {"queryset_class": CustomQuerySet,
            "index_background": True,
            "indexes": ["college", "major", "total_score", "net_score"]
            }

    kaohao = db.StringField(primary_key=True)
    password = db.StringField(required=True)
    college = db.StringField(required=True)
    major = db.StringField(required=True)
    subject1_code = db.StringField(required=True)
    subject1_score = db.IntField(required=True)
    subject2_code = db.StringField(required=True)
    subject2_score = db.IntField(required=True)
    subject3_code = db.StringField(required=True)
    subject3_score = db.IntField(required=True)
    subject4_code = db.StringField(required=True)
    subject4_score = db.IntField(required=True)

    net_score = db.IntField(required=True)
    total_score = db.IntField(required=True)

    def __str__(self):
        return "kaohao: " + self.kaohao + " score: " + str(self.total_score)

    @staticmethod
    def get(kaohao):
        users = User.objects(kaohao=kaohao)
        return users[0] if len(users) > 0 else None

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
        self.update(password=temp_password)
        return self

    def validate_password(self, password):
        return self.password == self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return md5((current_app.config['SECRET_KEY'] + password).encode(encoding='UTF-8')).hexdigest()

    @staticmethod
    def insert_new(info_list, password):
        (kaohao, college, major, first_name, first_score, second_name, second_score, third_name, third_score
         , fourth_name, fourth_score, total_score) = info_list
        user = User(kaohao=kaohao,
                    password=User.hash_password(password),
                    college=college,
                    major=major,
                    subject1_code=first_name,
                    subject1_score=first_score,
                    subject2_code=second_name,
                    subject2_score=second_score,
                    subject3_code=third_name,
                    subject3_score=third_score,
                    subject4_code=fourth_name,
                    subject4_score=fourth_score,
                    net_score=second_score + third_score + fourth_score,
                    total_score=total_score)
        user.save()
        return user
