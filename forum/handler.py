import json
from typing import Optional, Awaitable

import tornado.web
from aioredis import Redis
from peewee_async import Manager
from playhouse.shortcuts import model_to_dict

from databases import MysqlPool
from utils.utils import CJsonEncoder


class BaseHandler(tornado.web.RequestHandler):
    def set_400_status(self):
        self.set_status(400)

    def set_401_status(self):
        self.set_status(401)

    def set_403_status(self):
        self.set_status(403)


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

    def get_paginate_data(self):
        """获取分页信息"""
        current = self.get_argument("current", None)
        page_size = self.get_argument("pageSize", None)
        if not current:
            current = 1
        if not page_size:
            page_size = self.settings["default_page_size"]
        try:
            int(current), int(page_size)
        except ValueError:
            self.set_400_status()
            self.response(msg="参数错误", code=-1)
            return None, None
        else:
            return (int(current), int(page_size),)

    def response(self, data=None, code=200, msg=""):
        """查询单个数据库对象或其他类型data的返回格式"""
        if not data:
            self.finish(json.loads(json.dumps(dict(code=code, msg=msg), cls=CJsonEncoder)))
        else:
            self.finish(json.loads(json.dumps(dict(code=code, data=data, msg=msg), cls=CJsonEncoder)))

    def response_pagination(self, data=None, count=None, current=None, page_size=None, code=200, msg=""):
        if not data:
            self.finish(dict(data=[], count=count, current=current, page_size=page_size, code=code, msg=msg))
        results = []
        for d in data:
            dic = model_to_dict(d)
            results.append(dic)
        self.finish(json.loads(json.dumps(dict(code=code, count=count, current=current, page_size=page_size, data=results, msg=msg), cls=CJsonEncoder)))

    def response_multi_object(self, data=None, code=200, msg=""):
        """查询多个数据库对象返回格式"""
        if not data:
            self.finish(dict(data=[], code=code, msg=msg))
        results = []
        for d in data:
            dic = model_to_dict(d)
            results.append(dic)
        self.finish(json.loads(json.dumps(dict(code=code, data=results, msg=msg), cls=CJsonEncoder)))

    def form_invalid_response(self, form, msg):
        """表单校验不通过的返回格式"""
        err_data = {}
        for field in form.errors:
            err_data[field] = form.errors[field][0]
            self.response(data=err_data, msg=msg)

    @property
    def redis(self) -> Redis:
        return self.application.redis


    @property
    def db(self) -> Manager:
        """获取mysql链接"""
        return MysqlPool().get_manager
