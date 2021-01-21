import asyncio

import tornado
from tornado import web
from tornado.options import parse_command_line

from databases.redis import RedisPool
from forum.urls import urlpattern
from forum.settings import settings

from databases.mysql import database

import wtforms_json
import peewee_async


def make_app(loop):
    wtforms_json.init()
    apps = tornado.web.Application(urlpattern, debug=True, **settings)
    # 把loop传递过RedisPool获取一个链接
    apps.redis = RedisPool(loop=loop).get_conn()
    objects = peewee_async.Manager(database)
    database.set_allow_sync(False)
    apps.mysql = objects
    return apps


if __name__ == '__main__':
    try:
        parse_command_line()
        loop = asyncio.get_event_loop()
        app = make_app(loop)
        app.listen(8888)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
