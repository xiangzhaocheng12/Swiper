import json
import time
from hashlib import md5
import requests
from Swiper import config as cfg

# 第三方的对接逻辑最好独立出来
def send_sms(phonenum,vcode):
    args = {
        'appid': cfg.SD_APPID,
        'to': phonenum,
        'project': cfg.SD_PROJECT,
        'vars': json.dumps({'vcode':vcode}),
        'timestamp': int(time.time()),
        'sign_type': cfg.SD_SIGN_TYPE,
    }

    # 数字签名
    signature_str = \
        '&'.join([f'{k}={v}' for k, v in sorted(args.items())])
    string = f'{appid}{appkey}{signature_str}{appid}{appkey}'
    signature_str = hashlib.md5(string.encode('utf8')).hexdigest()
    args['signature'] = signature_str

    response = requests.post(api, data=args)
    print(response.content)
    print(response.status_code)
    data = {
        'code': 200,
        'data': '注册成功',
    }
