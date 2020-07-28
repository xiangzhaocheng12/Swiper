"""
    如果必须的参数都给全了, 还是返回错误提示,
    那么就把非必须参数都写进去
"""
import time
import requests
import json
import hashlib

api = 'https://api.mysubmail.com/message/xsend'

appid = '52461'
appkey = 'b2a7e3b4f77d220a5c26f3625db7b368'

# 总共四个参数
args = {
    'appid': appid,
    'to': '13567943726',
    'project': 'axSpR',
    'vars': json.dumps({'code': '123456', 'time': '5分钟'}),
    'timestamp': int(time.time()),
    'sign_type': 'md5',
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
