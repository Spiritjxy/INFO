# 创建配置类
import redis


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


# 开发者模式配置
class DevelopConfig(Config):
    pass


# 生产模式配置
class ProductConfig(Config):
    # 关闭调试信息
    DEBUG = False


# 测试模式配置
class TestConfig(Config):
    # 开启测试模式
    TESTING = True


# 提供统一访问入口
config_dict = {
    "develop": DevelopConfig,
    "product": ProductConfig,
    "test": TestConfig
}
