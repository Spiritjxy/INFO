from flask import current_app
from flask import render_template

from . import index_blue
from info import redis_store


@index_blue.route('/')
def index():
    redis_store.set('name', 'jxy')
    print(redis_store.get('name'))
    return render_template('news/index.html')


# 网站logo图片处理,浏览器向每个网站请求数据的时候会默认调用GET 向/favicon.ico接口,获取logo图片
# current_app.send_static_file('图片'), 会自动去static文件中寻找该图片,返回response对象
@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
