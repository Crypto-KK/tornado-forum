from peewee import Model
from loguru import logger
from peewee_async import execute
from databases import MysqlPool, RedisPool


class BaseService:
    model: Model = None  # ORM类
    _service = dict()  # 类实例集合

    @classmethod
    def instance(cls):
        """单例，对实例保存_service中避免多次调用重新创建"""
        """Method  instance
        :return: cls
        """
        instance = cls._service.get(cls.__name__, None)
        if not instance:
            instance = cls.__new__(cls)
            cls._service.setdefault(cls.__name__, instance)
        return instance

    @staticmethod
    async def execute(sql):
        """有些复杂的sql，orm用户起来不太方便，直接运行sql"""
        try:
            return await execute(sql)
        except Exception as e:
            logger.exception(str(e))
            return None

    async def insert(self, **kwargs):
        """peewee create方法保存数据"""
        try:
            return await self.db.create(self.model, **kwargs)
        except Exception as e:
            logger.exception(str(e))
            return None

    async def update(self, data):
        """更新一条数据
        :param Model
        """
        try:
            return await self.db.update(data)
        except self.model.DoesNotExist:
            return None
        except Exception as e:
            logger.exception(str(e))
            return None

    async def find_one(self, *args, **kwargs):
        """查找一条数据, 当返回多条数据会报错"""
        if not args:
            return await self.db.get(self.model, *args, **kwargs)
        res = await self.find(*args, **kwargs)
        if len(res) > 1:
            raise Exception("find multiple data")
        elif len(res) == 1:
            return res[0]
        return None

    async def find(self, *args, **kwargs):
        """查询指定字段，查找多条数据"""
        if not args:
            raise Exception("fields is empty")

        sql = self.model.select(*[getattr(self.model, k) for k in args])
        for key, val in kwargs.items():
            sql = sql.where(getattr(self.model, key) == val)
        try:
            return await self.db.execute(sql)
        except Exception as e:
            logger.exception(str(e))
            return []

    @property
    def db(self):
        """获取mysql链接"""
        return MysqlPool().get_manager

    @property
    def redis(self):
        return RedisPool().get_conn()
