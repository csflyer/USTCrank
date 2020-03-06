from wtforms.fields import StringField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm

# 验证码字段
class VerifyCodeField(StringField):
    def __call__(self, *args, **kwargs):
        html = super(VerifyCodeField, self).__call__(*args, **kwargs)
        addition = '<span id="code-change" class="input-group-addon">' \
                   '<img id="validate_img" src="/static/captcha.jpg">' \
                   '</span>'
        return "<div class='input-group'>" + html + addition + "</div>"


# 登录表单
class LoginForm(FlaskForm):
    kaohao = StringField('准考证号', validators=[DataRequired(), Length(15, 15)])
    name = StringField('考生姓名', validators=[DataRequired(), Length(1, 5)])
    id = StringField('身份证号', validators=[DataRequired(), Length(18, 18)])
    code = VerifyCodeField('验证码(首次查询才点击刷新验证码,非首次随便填四位)', validators=[DataRequired(), Length(4,4)])
    submit = SubmitField('提交查询')
