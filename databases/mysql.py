import peewee_async

database = peewee_async.MySQLDatabase(
    "tornado_forum",
    host="127.0.0.1",
    port=3306,
    user="root",
    password="998219"
)
