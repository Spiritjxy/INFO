from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict
import logging

# 创建db，为了别的文件可以导入
db = SQLAlchemy()

redis_store = None


def create_app(config_name):
    app = Flask(__name__)

    # 根据manager传入的配置名称，取出不同的配置类
    Config = config_dict.get(config_name)

    # 调用日志
    log(Config.LEVEL)

    # 将配置类信息加载到app
    app.config.from_object(Config)

    # 创建数据库，关联app
    db.init_app(app)

    # 创建redis对象
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

    # 开启CSRF保护
    CSRFProtect(app)

    # 开启Session
    Session(app)

    # 注册index蓝图
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)

    # 注册passport蓝图
    from info.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    return app


def log(level):
    # 设置日志的记录等级
    logging.basicConfig(level=level)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
