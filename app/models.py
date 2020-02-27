from . import db
from sqlalchemy.exc import IntegrityError

# ORM 数据类
class User(db.Model):
    __tablename__ = 'users'

    kaohao = db.Column(db.String(18), unique=True, primary_key=True)
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

    @staticmethod
    def insert_new(info_list):
        (kaohao, college, major, first_name, first_score, second_name, second_score, third_name, third_score
         , fourth_name, fourth_score, total_score) = info_list
        user =  User(kaohao=kaohao,
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
