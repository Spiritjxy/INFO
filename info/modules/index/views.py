from flask import current_app, jsonify
from flask import render_template
from flask import session

from info.models import User
from info.utils.response_code import RET
from . import index_blue
from info import redis_store


@index_blue.route('/')
def index():
    # 获取用户
    user_id = session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    data = {
        'user_info': user.to_dict() if user else ''
    }

    return render_template('news/index.html', data=data)


# 网站logo图片处理,浏览器向每个网站请求数据的时候会默认调用GET 向/favicon.ico接口,获取logo图片
# current_app.send_static_file('图片'), 会自动去static文件中寻找该图片,返回response对象
@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
