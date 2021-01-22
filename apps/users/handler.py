from apps.users.forms import SmsCodeForm, RegisterForm, LoginForm
from apps.users.models import User
from forum.handler import BaseHandler
from apps.users.service import UserService
from forum.settings import settings
from datetime import datetime
import jwt


class SmsHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        form = self.get_form(SmsCodeForm)
        if form.validate():
            mobile = form.mobile.data
            code = "6666"
            await self.redis.set(f"{mobile}_{code}", 1, expire=10 * 60)
            self.response(msg="发送成功")
        else:
            self.set_status(400)
            self.form_invalid_response(form, "发送失败")


class LoginHandler(BaseHandler):
    """登录"""
    async def post(self):
        form = self.get_form(LoginForm)
        if form.validate():
            mobile = form.mobile.data
            password = form.password.data
            try:
                user = await UserService.instance().get_user_by_mobile(mobile=mobile)
                if not user.password.check_password(password):
                    self.set_status(400)
                    self.response(msg="密码错误")
                else:
                    payload = {
                        "userid": user.id,
                        "nickname": user.nickname,
                        "exp": datetime.utcnow()
                    }
                    token = jwt.encode(payload, settings['jwt']['secret_key'], algorithm='HS256')
                    self.response(data={
                        "token": token,
                        "id": user.id
                    }, msg="登录成功")

            except User.DoesNotExist:
                self.set_status(400)
                self.response(msg="用户不存在")


class RegisterHandler(BaseHandler):
    """注册"""
    async def post(self, *args, **kwargs):
        form = self.get_form(RegisterForm)
        if form.validate():
            mobile = form.mobile.data
            code = form.code.data
            password = form.password.data

            # 验证码验证
            redis_key = f"{mobile}_{code}"
            if not await self.application.redis.get(redis_key):
                self.set_status(400)
                self.response(msg="验证码错误")
            else:
                # 手机号是否重复
                try:
                    await UserService.instance().get_user_by_mobile(mobile=mobile)
                    self.set_status(400)
                    self.response(msg="用户已存在")
                except User.DoesNotExist:
                    user = await UserService.instance().insert_user(mobile=mobile, password=password)
                    self.response(data=user, msg="注册成功")
        else:
            self.set_status(400)
            self.form_invalid_response(form, "注册失败")
