import random
import re

from flask import current_app, jsonify
from flask import make_response
from flask import request

from info import constants
from info import redis_store
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blue
from info.libs.yuntongxun.sms import CCP


# 发送短信验证码
@passport_blue.route('/sms_code', methods=["POST"])
def get_sms_code():
    # 获取参数
    mobile = request.json.get('mobile')
    image_code = request.json.get('image_code')
    image_code_id = request.json.get('image_code_id')
    # 判断参数是否为空
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 判断手机号格式
    if not re.match('1[3456789]\\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')
    # 通过验证码id取出验证码
    try:
        image = redis_store.get('image_code:%s' % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取图片验证码失败')
    # 判断验证码是否过期
    if not image:
        return jsonify(errno=RET.NODATA, errmsg='图片验证码过期')
    # 判断输入的验证码是否正确
    if image_code.upper() != image.upper():
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码不正确')
    # 生成短信验证码
    sms_code = '%06d' % random.randint(0, 999999)
    # 保存验证码在redis
    try:
        redis_store.set('sms_code:%s' % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='保存短信验证码失败')
    # 调用云通讯发送短信
    try:
        ccp = CCP()
        result = ccp.send_template_sms('18516952650', ['1234', 5], 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg='调用云通讯失败')
    if result != 0:
        return jsonify(errno=RET.DATAERR, errmsg='发送短信失败')

    return jsonify(errno=RET.OK, errmsg='发送短信成功')


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
