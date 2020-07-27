from django.shortcuts import render

# Create your views here.
from libs.http_ import render_json
from social import logics


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
    pass


def fans(request):
    pass


def friends(request):
    pass
