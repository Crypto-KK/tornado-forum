from databases.mysql import MysqlPool
from peewee import *
from datetime import datetime


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now, verbose_name="add time")
    updated_at = DateTimeField(default=datetime.now, verbose_name='更新时间')

    def save(self, force_insert=False, only=None):
        if self._get_pk_value() is None:
            self.add_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        database = MysqlPool().get_conn
        legacy_table_names = False
