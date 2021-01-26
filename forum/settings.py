import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "static_path": "../static",
    "static_url_prefix": "/static/",
    "template_path": "templates",
    "MEDIA_ROOT": os.path.join(BASE_DIR, "media"),
    "db": {
        "database": "tornado_forum",
        "host": "127.0.0.1",
        "user": "root",
        "password": "998219",
        "port": 3306,
        "charset": "utf8mb4",
        "max_connections": 10
    },
    "redis": {
        "host": "localhost",
        "port": 6379
    },
    "jwt": {
        "secret_key": "secret"
    }
}

