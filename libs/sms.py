import json
import time
from hashlib import md5
import requests
from Swiper import config as cfg

# 第三方的对接逻辑:
#       注意: 第三方的模块对接最好独立出来
def send_sms(phonenum,vcode,time_str):
    """发送验证码"""
    #   构造参数
    args = {
        'appid': cfg.SD_APPID,
        'to': phonenum,
        'project': cfg.SD_PROJECT,
        'vars': json.dumps({'code':vcode,'time':time_str}),
        'timestamp': int(time.time()),
        'sign_type': cfg.SD_SIGN_TYPE,
    }

    # 数字签名
    signature_str = \
        '&'.join([f'{k}={v}' for k, v in sorted(args.items())])
    # 这里别填错了!!!
    string = f'{cfg.SD_APPID}{cfg.SD_APPKEY}{signature_str}{cfg.SD_APPID}{cfg.SD_APPKEY}'
    signature_str = md5(string.encode('utf8')).hexdigest()

    # 将签名添加到列表中
    args['signature'] = signature_str

    response = requests.post(cfg.SD_API, data=args)

    result = response.json()

    return result