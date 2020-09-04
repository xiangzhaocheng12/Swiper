import json
from django.http import HttpResponse
from django.conf import settings

from common import stat


def render_json(data=0, code=stat.OK):
    """前后端接口定义"""
    result = {
        'data': data,
        'code': code
    }
    if settings.DEBUG == True:
        # 调试时, 将json 数据转成缩进的数据
        # indent: 缩进的长度
        # sort_keys: 表示是否格式化
        # sort_keys = False   使数据不转化为 ASCII 码
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        # 线上环境, 将返回值转化成紧凑格式
        json_str = json.dumps(result, ensure_ascii=False, separators=(',', ':'))
    # 必须返回一个HttpResponse的对象, 因为JsonResponse继承自 HttpResponse
    return HttpResponse(json_str,content_type='application/json')
