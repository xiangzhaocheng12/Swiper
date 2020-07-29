import re
import random
import logging
# 先编译一些
# 全都换成自己重写的 redis
from libs.cache import rds

from libs.sms import send_sms
from common.keys import VCODE_K
from tasks import celery_app

inf_logger = logging.getLogger('inf')
P_PHONENUM = re.compile(r'^1[3456789]\d{9}$')


def is_phonenum(phonenum):
    # 检查是否是有效的数字
    # match 表示从头开始匹配
    return True if P_PHONENUM.match(phonenum) else False


def gen_randcode(length):
    """产生指定长度的随机码"""
    chars = random.choices('012345678',k = length)
    return ''.join(chars)

# 异步化进行发送
@celery_app.task
def send_vcode(phonenum):
    """向用户手机发送验证码"""
    key = VCODE_K % phonenum

    # 检查十五分钟之内是否被该用户发送验证码, 防止恶意获取
    if rds.get(key):
        return True

    vcode = gen_randcode(6)  # 定义验证码
    time_str = '10分钟'
    print('====================')
    print(vcode)
    # result = send_sms(phonenum, vcode,time_str)  # 发送验证码
    result = {'status':'success'}
    if result.get('status') == 'success':
        # 这个是一个本地内存,不是一个通用的内存
        # 需要引入 Redis 到 Django 中
        rds.set(key, vcode, 900)  # 多为用户保留五分钟
        inf_logger.debug('vcode:%s' %vcode)
        return True
    else:
        return False
