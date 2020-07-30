from django.shortcuts import render

# Create your views here.
import logging
from libs.http_ import render_json
from social import logics
from social.models import Friend
from vip.logics import require_perm

inf_logger = logging.getLogger('inf')

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
    is_matched = logics.like_someone(request.uid, sid)
    inf_logger.info(f'{request.uid} like {sid}')
    return render_json(data=is_matched)


def dislike(request):
    '''不喜欢'''
    sid = int(request.POST.get('sid'))
    # 对用户进行匹配
    logics.dislike_someone(request.uid, sid)
    inf_logger.info(f'{request.uid} dislike {sid}')
    return render_json(data=None)


@require_perm('superlike')
def superlike(request):
    '''超级喜欢'''
    sid = int(request.POST.get('sid'))
    # 返回是否匹配的结果
    is_matched = logics.super_like_someone(request.uid, sid)
    inf_logger.info(f'{request.uid} superlike {sid}')
    return render_json(data=is_matched)


@require_perm('rewind')
def rewind(request):
    '''反悔'''
    # 能不依赖前端, 就尽量不依赖前端
    logics.rewind_last_swipe(request.uid)
    return render_json()


@require_perm('show_fans')
def show_fans(request):
    '''查看粉丝'''
    # 超级特权的一个接口
    fans = logics.find_fans(request.uid)
    result = [user.to_dict() for user in fans]
    return render_json(result)


def friends(request):
    '''查看好友'''
    friends = Friend.my_friends(request.uid)
    # 类似前面的方式把结果弄出来 列表里面包着多个字典
    result = [frd.to_dict() for frd in friends]
    return render_json(data=result)


def hot_rank(request):
    '''热度排名'''
    rank_data = logics.top_n(50)
    return render_json(rank_data)