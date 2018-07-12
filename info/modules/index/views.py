from flask import current_app, jsonify
from flask import render_template
from flask import request
from flask import session

from info.models import User, News, Category
from info.utils.response_code import RET
from . import index_blue
from info import redis_store


# 首页新闻
@index_blue.route('/newslist')
def get_newslist():
    # 获取参数
    page = request.args.get('page', 1)  # 当前页数id
    cid = request.args.get('cid', 1)  # 当前分类id
    per_page = request.args.get('per_page', 10)  # 每页新闻个数
    # 参数强转
    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
        cid = 1
        per_page = 10
    # 获取新闻
    try:
        filters = []
        if cid != 1:
            filters.append(News.category_id == cid)
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询新闻失败')

    items = paginate.items

    news_list = []
    for news in items:
        news_list.append(news.to_dict())

    data = {
        'total_page': paginate.pages,
        'news_li': news_list
    }

    return jsonify(errno=RET.OK, errmsg='获取新闻成功', data=data)


# 首页内容
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
