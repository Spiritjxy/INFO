from flask import current_app, jsonify
from flask import make_response
from flask import request

from info import constants
from info import redis_store
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blue


# 生成图片验证码
@passport_blue.route('/image_code')
def get_image_code():
    # 获取参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')
    # 生成图片验证码
    name, text, image_code = captcha.generate_captcha()
    # 保存到数据库
    try:
        redis_store.set('image_code:%s' % cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete('image_code:%s' % pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存验证码失败')

    resp = make_response(image_code)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp
