from django.shortcuts import render

# Create your views here.
from libs.http_ import render_json
from social import logics
from social.models import Friend


def rcmd(request):
    '''推荐用户'''
    users = logics.rcmd(request.uid)
    # 列表生成式
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢'''
    sid = int(request.POST.get('sid'))
    # 返回是否匹配的结果
    is_matched = logics.like_someone(request.uid,sid)
    return render_json(data=is_matched)


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    # 对用户进行匹配
    logics.dislike_someone(request.uid,sid)
    return render_json(data = None)

def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    # 返回是否匹配的结果
    is_matched = logics.super_like_someone(request.uid,sid)
    return render_json(data=is_matched)


def rewind(request):
    '''反悔'''
    pass


def fans(request):
    '''查看粉丝'''
    pass


def friends(request):
    '''查看好友'''
    friends = Friend.my_friends(request.uid)
    # 类似前面的方式把结果弄出来 列表里面包着多个字典
    result = [frd.to_dict() for frd in friends]
    return render_json(data = result)
