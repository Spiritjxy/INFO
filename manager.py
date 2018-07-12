from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import config_dict

app = Flask(__name__)

# 将配置类信息加载到app
app.config.from_object(config_dict)

Config = config_dict['develop']

# 创建数据库，关联app
db = SQLAlchemy(app)

# 创建redis对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 开启CSRF保护
CSRFProtect(app)

# 开启Session
Session(app)

# 创建manager，关联app
manager = Manager(app)
# 关联app，db
Migrate(app, db)
# 添加操作命令
manager.add_command('db', MigrateCommand)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    manager.run()
