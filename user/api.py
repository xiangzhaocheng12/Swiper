import json

from django.core.cache import cache
# 这个是自己写的 render返回函数, 用来代替原先的JsonResponse()

from libs.http_ import render_json

# Create your views here.
from common import keys
from user import logics
from user.models import User, Profile
from common import stat


def fetch(request):
    """ 提交手机号 """
    # GET 是一个字典类型
    phonenum = request.GET.get('phonenum')
    # 检查用户手机号是否正确
    if logics.is_phonenum(phonenum):
        # 如果手机号正确的话, 发送验证码, 判断是否发送成功
        if logics.send_vcode(phonenum):
            return render_json()
    # 如果手机号验证失败的话, 直接返回验证码发送失败
    return render_json(code=stat.SEND_FAILD)


def submit(request):
    """提交验证码, 完成登陆、注册"""
    # strip() 用来取出字符串两端空格
    phonenum = request.POST.get('phonenum','').strip()
    vcode = request.POST.get('vcode','').strip()

    # 从缓存获取验证码
    key = keys.VCODE_K % phonenum
    cached_vcode = cache.get(key)

    # 检查验证码
    # vcode: 用户提交的验证码,     cached_vcode: 缓存中的验证码
    # 需要考虑下面这种情况:
    #       None == None
    if vcode and vcode == cached_vcode:
        # 根据手机号获取用户
        # flask 里面不是 objects, 而是一个query
        # get:只能获取一个
        try:
            user = User.objects.get(phonenum=phonenum)
        # 这里不能只写一个except, 需要精确的写上一个异常
        except User.DoesNotExist:
            # user = User()
            # ....
            # user.save()
            # 法2：
            user = User.objects.create(phonenum = phonenum,nickname = phonenum)
            Profile.objects.create(uid=user.id)

        # 通过 Session 记录用户登陆状态
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return render_json(code=stat.VCODE_ERR)


def show(request):
    uid = request.session.get('uid')
    profile = Profile.objects.get(uid = uid)
    return render_json(data = profile.to_dict())


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

    data = {
        "data": None
    }
    return render_json()


def qn_token(request):
    return render_json()
