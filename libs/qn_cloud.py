import time
import json
from qiniu import Auth
from urllib.parse import urlencode
from Swiper import config as cfg


# 还需要定义一个policy的规则, 这个根据官方文档来进行
def gen_policy(uid, key):
    ''' 产生一个上传策略'''
    url = '%s/%s' % (cfg.QN_HOST, key)
    return {
        # 详细的参数文档:
        # https://developer.qiniu.com/kodo/manual/1206/put-policy
        'scope': f"{cfg.QN_BUCKET}：{key}",  # 指定上传的目标资源空间 Bucket 和资源键 Key（最大为 750 字节）
        # 截止时间需要转化为 东八区的时间
        'deadline': int(time.time()) + 3600 * 8 + cfg.QN_TIMEOUT,  # 时间戳
        'returnBody': json.dumps({'code': 0, 'data': url}),  #
        # 这个没有域名的话就用服务器的地址
        'callbackUrl': 'http://39.106.162.75/qiniu/callback',
        'callbackHost': '39.106.162.75',
        # callbackBody 需要使用json的格式, 这里用urlencode 进行处理
        'callbackBody': urlencode({'uid': uid, 'key': key}),  # 这里使用魔法变量可能会出错
        'callbackBodyType': 'application/x-www-form-urlencoded',
        'forceSaveKey': True,
        # 文件强制保存的名字
        'saveKey': key,
        # 文件的大小的单位为bytes, 这里设置文件的最大值
        'fsizeLimit': 10485760,  # 10MB
        # image/*: 只允许上传image类型
        'mimeLimit': 'image/*',
    }


def get_token(uid, key):
    '''产生一个上传凭证(Token)'''
    qn_auth = Auth(cfg.QN_ACCESS_KEY, cfg.QN_SECRET_KEY)
    # 定义了一些另外的规则
    policy = gen_policy(uid, key)
    token = qn_auth.upload_token(cfg.QN_BUCKET, key, cfg.QN_TIMEOUT, policy)
    return token
