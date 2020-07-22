import json

from django.http import JsonResponse
from django.shortcuts import render
import time
import requests
import json
import hashlib


# Create your views here.
from user import logics


def fetch(request):
    """ 提交手机号 """
    # GET 是一个字典类型
    phonenum = request.GET.get('phonenum')

    # 检查用户手机号是否正确
    if logics.is_phonenum(phonenum):
        logics.send_sms(phonenum)

    else:

        return JsonResponse(data)


def submit(request):
    phonenum = request.GET.get('phonenum')
    vcode = request.GET.get('vcode')
    # 需要返回的数据
    code = 0
    data = {
        "code": 0,
        "data": {
            'id': 1002,
            'nickname': 'Miao',
            'birthday': '2000-01-01',
            'gender': 'male',
            'location': '北京',
            'avatar': 'http://xxx.com/a/b/c.png'
        }
    }
    return JsonResponse(data)


def show(request):
    data = {
        "code":0,
        "data":{
            "id":1002,
            "dating_gender":"female",
            "dating_location":"北京",
            "max_distance":10,
            "min_distance":1,
            "max_dating_age":50,
            "min_dating_age":20,
            "vibration":False,
            "only_matched":False,
            "auto_play":False,
        }
    }
    return JsonResponse(data)


def update(request):
    nickname = request.POST.get('nickname')
    birthday = request.POST.get('birthday')
    gender = request.POST.get('gender')
    location = request.POST.get('location')
    dating_gender = request.POST.get('dating_gender')
    dating_location = request.POST.get('dating_location')
    max_distance = request.POST.get('max_distance')
    min_distance = request.POST.get('min_distance')
    max_dating_age = request.POST.get('max_dating_age')
    min_dating_age = request.POST.get('min_dating_age')
    vibration = request.POST.get('vibration')
    only_matched = request.POST.get('only_matched')
    auto_play = request.POST.get('auto_play')

    data  = {
        "data":None
    }
    return JsonResponse(data)


def qn_token(request):
    return JsonResponse(data = {'a':123})