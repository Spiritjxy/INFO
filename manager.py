from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)


# 创建配置类
class Config(object):
    DEBUG = True
    SECRET_KEY = 'jxy'

    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/infomation'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis配置信息
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # Session配置信息
    SESSION_TYPE = 'redis'  # 设置存储类型
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 设置数据库连接
    SESSION_USE_SIGNER = True  # 置签名存储
    SESSION_PERMANENT = False  # 设置session需要过期
    PERMANENT_SESSION_LIFETIME = 86400 * 2  # 设置session过期时间,单位是秒


# 将配置类信息加载到app
app.config.from_object(Config)

# 创建数据库，关联app
db = SQLAlchemy(app)

# 创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 开启CSRF保护
CSRFProtect(app)

# 开启Session
Session(app)

# 数据库迁移配置
Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    manager.run()
