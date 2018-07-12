from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# 创建配置类
class Config(object):
    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/infomation'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


# 将配置类信息加载到app
app.config.from_object(Config)
# 创建数据库，关联app
db = SQLAlchemy(app)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run(debug=True)
