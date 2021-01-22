from loguru import logger
from peewee_async import Manager
from peewee_async import PooledMySQLDatabase

from forum.settings import settings


_settings = settings['db']

class MysqlPool:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            logger.debug("init mysql pool")
            cls.conn = PooledMySQLDatabase(
                database=_settings['database'],
                host=_settings['host'],
                password=_settings['password'],
                port=_settings['port'],
                user=_settings['user'],
                max_connections=_settings['max_connections'],
                charset=_settings['charset']
            )
            cls.manager = Manager(cls.conn)
            cls._instance = super(MysqlPool, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def get_conn(self):
        return self.conn

    @property
    def get_manager(self):
        return self.manager
