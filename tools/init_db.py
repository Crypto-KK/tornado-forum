from apps.community.models import CommunityGroup
from apps.users.models import User

from peewee import MySQLDatabase

database = MySQLDatabase("tornado_forum", host="127.0.0.1", port=3306, user="root", password="998219")


def init():
    database.create_tables([CommunityGroup])


if __name__ == '__main__':
    init()
