from flask import current_app, jsonify
from flask import render_template
from flask import session

from info.models import User, News, Category
from info.utils.response_code import RET
from . import index_blue
from info import redis_store


@index_blue.route('/')
def index():
    # 获取用户信息
    user_id = session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 获取点击排行新闻
    try:
        news = News.query.order_by(News.clicks.desc()).limit(10)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取点击排行新闻失败')
    news_list = []
    for new in news:
        news_list.append(new.to_dict())

    # 获取新闻分类
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询分类失败')
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())

    # 返回的所有数据字典
    data = {
        'user_info': user.to_dict() if user else '',
        'news_list': news_list,
        'category_list': category_list
    }

    return render_template('news/index.html', data=data)


# 网站logo图片处理,浏览器向每个网站请求数据的时候会默认调用GET 向/favicon.ico接口,获取logo图片
# current_app.send_static_file('图片'), 会自动去static文件中寻找该图片,返回response对象
@index_blue.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
