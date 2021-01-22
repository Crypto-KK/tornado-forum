import functools
import jwt

from apps.users.models import User
from forum.handler import BaseHandler
from forum.settings import settings


def authenticated_async(method):

    @functools.wraps(method)
    async def wrapper(self: BaseHandler, *args, **kwargs):
        header = self.request.headers.get("Authorization", None)
        if header:
            try:
                token = header.split(" ")[1]
            except Exception:
                self.set_status(401)
                self.response(msg="token解析错误", code=0)
            try:
                payload = jwt.decode(token, settings['jwt']['secret_key'], leeway=1, options={"verify_exp": False}, algorithms="HS256")
                user_id = payload['userid']

                # 从数据库获取
                try:
                    user = await self.db.get(User, id=user_id)
                    self._current_user = user
                    await method(self, *args, **kwargs)
                except User.DoesNotExist:
                    self.set_status(401)
                    self.response(msg="用户查找失败", code=0)

            except jwt.exceptions.ExpiredSignatureError:
                self.set_status(401)
                self.response(msg="token过期失效", code=0)
            except jwt.exceptions.InvalidSignatureError:
                self.set_status(401)
                self.response(msg="token错误", code=0)
        else:
            self.set_status(401)
            self.response(msg="未携带token", code=0)

    return wrapper
