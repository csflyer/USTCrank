from wtforms.fields import StringField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm

class VerifyCodeField(StringField):
    def __call__(self, *args, **kwargs):
        html = super(VerifyCodeField, self).__call__(*args, **kwargs)
        addition = '<span id="code-change" class="input-group-addon">' \
                   '<img id="validate_img" src="/captcha">' \
                   '</span>'
        return html + addition

class LoginForm(FlaskForm):
    kaohao = StringField('准考证号', validators=[DataRequired(), Length(1, 5)])
    name = StringField('考生姓名', validators=[DataRequired(), Length(1, 5)])
    id = StringField('身份证号', validators=[DataRequired(), Length(18, 18)])
    code = VerifyCodeField('验证码', validators=[DataRequired(), Length(4,10)])
    submit = SubmitField('提交查询',)