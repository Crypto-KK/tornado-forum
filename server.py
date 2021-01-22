import asyncio

import tornado
from tornado import web
from tornado.options import parse_command_line
from loguru import logger

from databases.redis import RedisPool
from forum.urls import urlpattern
from forum.settings import settings


import wtforms_json


def make_app(loop):
    logger.add("logs/api.log")
    wtforms_json.init()
    apps = tornado.web.Application(urlpattern, debug=True, **settings)
    # 把loop传递过RedisPool获取一个链接
    apps.redis = RedisPool(loop=loop).get_conn()
    return apps


if __name__ == '__main__':
    try:
        logger.info("server start")
        parse_command_line()
        loop = asyncio.get_event_loop()
        app = make_app(loop)
        app.listen(8888)
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("server stop")
