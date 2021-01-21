from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

MOBILE_REGEX = "/^1[3-9]\d{9}$/"


class SmsCodeForm(Form):
    mobile = StringField("手机号", validators=[
        DataRequired(message="请输入手机号"),
        # Regexp(MOBILE_REGEX, message="请输入合法手机号")
    ])


class RegisterForm(Form):
    mobile = StringField("手机号", validators=[
        DataRequired(message="请输入手机号"),
        # Regexp(MOBILE_REGEX, message="请输入合法手机号")
    ])
    code = StringField("验证码", validators=[
        DataRequired(message="请输入验证码"),
        Length(min=4, max=4, message="验证码长度必须为4")
    ])
    password = StringField("密码", validators=[
        DataRequired(message="请输入密码"),
        Length(min=6, max=12, message="密码长度6-12")
    ])
