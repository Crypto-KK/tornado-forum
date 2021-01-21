import json
from typing import Optional, Awaitable

import tornado.web
from aioredis import Redis
from peewee_async import Manager


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_json_data(self):
        try:
            json_data = self.request.body.decode("utf-8")
            json_data = json.loads(json_data)
            return json_data
        except json.JSONDecodeError:
            raise tornado.web.HTTPError(400)

    def get_form(self, form):
        param = self.get_json_data()
        new_form = form.from_json(param)
        return new_form

    def response(self, data=None, code=200, msg=""):
        if not data:
            self.finish(dict(code=code, msg=msg))
        else:
            self.finish(dict(code=code, data=data, msg=msg))

    def form_invalid_response(self, form, msg):
        err_data = {}
        for field in form.errors:
            err_data[field] = form.errors[field][0]
            self.response(data=err_data, msg=msg)

    @property
    def redis(self) -> Redis:
        return self.application.redis


    @property
    def mysql(self) -> Manager:
        return self.application.mysql
