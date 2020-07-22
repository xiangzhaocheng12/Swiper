import re
import random

# 先编译一些
from django.core.cache import cache

from Swiper.libs.sms import send_sms

P_PHONENUM = re.compile(r'^1[3456789]\d{9}$')


def is_phonenum(phonenum):
    # 检查是否是有效的数字
    # match 表示从头开始匹配
    return True if P_PHONENUM.match(phonenum) else False


def gen_randcode(length):
    """产生指定长度的随机码"""
    random.choice
    random.


def send_vcode(phonenum):
    """向用户手机发送验证码"""
    key = 'Vcode-%s' % phonenum

    # 检查十五分钟之内是否被该用户发送验证码, 防止恶意获取
    if cache.get(key):
        return True

    vcode = gen_randcode(6)  # 定义验证码
    result = send_sms(phonenum, vcode)  # 发送验证码

    if result.get('status') == 'success':
        cache.set(key, vcode, 900)  # 多为用户保留五分钟
        return True
    else:
        return False
