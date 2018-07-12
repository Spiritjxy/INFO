from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict

# 创建db，为了别的文件可以导入
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    Config = config_dict(config_name)

    # 将配置类信息加载到app
    app.config.from_object(Config)

    # 创建数据库，关联app
    db.init_app(app)

    # 创建redis对象
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

    # 开启CSRF保护
    CSRFProtect(app)

    # 开启Session
    Session(app)

    return app
