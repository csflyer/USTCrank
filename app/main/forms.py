from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import Length, DataRequired
from flask_wtf import FlaskForm


# 封装验证码输入框
class VerifyCodeField(StringField):
    def __call__(self, *args, **kwargs):
        html = super(VerifyCodeField, self).__call__(*args, **kwargs)
        addition = '<span id="code-change" class="input-group-addon">' \
                   '<img id="validate_img" src="/captcha">' \
                   '</span>'
        # html 是一个Markup对象，直接拼接会将我们构造的html转义，从而无法显示图片
        # 这里将其转成字符串再拼接即可
        return "<div class='input-group'>" + str(html) + addition + "</div>"


# 首页登录表单
class LoginForm(FlaskForm):
    title = "登陆"

    kaohao = StringField('准考证号(首次登陆请先点击上面的注册查分)', validators=[DataRequired(), Length(15, 15)])
    password = PasswordField("查询密码", validators=[DataRequired(), Length(6, 20)])
    submit = SubmitField("登录查询")


# 成绩查询表单
class CJCXForm(FlaskForm):
    title = "查询成绩"

    kaohao = StringField('准考证号', validators=[DataRequired(), Length(15, 15)])
    name = StringField('考生姓名', validators=[DataRequired(), Length(1, 5)])
    id = StringField('身份证号', validators=[DataRequired(), Length(18, 18)])
    password = PasswordField("查询密码(后面查询排名用 6-20位)", validators=[DataRequired(), Length(6, 20)])
    code = VerifyCodeField('验证码', validators=[DataRequired(), Length(4, 4)])
    submit = SubmitField("查询成绩")


# 用于非登录状态找回密码
class ResetPasswordForm(FlaskForm):
    title = "找回密码"

    kaohao = StringField('准考证号', validators=[DataRequired(), Length(15, 15)])
    name = StringField('考生姓名', validators=[DataRequired(), Length(1, 5)])
    id = StringField('身份证号', validators=[DataRequired(), Length(18, 18)])
    password = PasswordField("新查询密码(6-20位)", validators=[DataRequired(), Length(6, 20)])
    code = VerifyCodeField('验证码', validators=[DataRequired(), Length(4, 4)])
    submit = SubmitField("修改密码")


# 用于登录状态修改密码
class SimpleResetPwForm(FlaskForm):
    title = "修改密码"

    password = PasswordField("新查询密码(6-20位)", validators=[DataRequired(), Length(6, 20)])
    submit = SubmitField("修改密码")