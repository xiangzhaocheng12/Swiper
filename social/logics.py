import datetime

from common import keys
from libs.cache import rds
from social.models import Swiped, Friend
from user.models import Profile, User
from django.db.utils import IntegrityError


def rcmd(uid):
    '''推荐滑动用户'''
    my_profile = Profile.objects.get(id=uid)
    today = datetime.datetime.today()
    # 注意类型转化:datetime.timedelta !!!
    earliest_date = today - datetime.timedelta(my_profile.max_dating_age * 365)  # 最早出生日期
    lasted_birthday = today - datetime.timedelta(my_profile.min_dating_age * 365)  # 最晚出生日期


    # 需要排除已经划过的人
    # values_list() 用来取出指定的字段, flat  = True 表示
    # 如果不使用 values_list()的话, 会取出所有的
    # select sid from Swiped where uid=1002;
    sid_list = Swiped.objects.filter(uid = uid).values_list('sid',flat = True)

    # 取出符合条件的用户
    # select * from xx limit 20;
    # select * from xx limit(20,30);
    users = User.objects.filter(
        location=my_profile.dating_location,
        gender=my_profile.dating_gender,
        birthday__gte=earliest_date,
        birthday__lte=lasted_birthday,
    # 排除所有带有滑动记录的 id
    ).exclude(id__in=sid_list)[:20]  # 这里会转化成一个limit 语句

    return users


def like_someone(uid, sid):
    '''喜欢(右划)某人'''
    # 1. 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='like')
    #
    except IntegrityError:
        # 重复滑动时, 直接返回当前用户是否已匹配成好友
        return Friend.is_friends(uid, sid)

    # 2. 检查对方是否右划或者上划过自己
    # 这里的uid  和  sid 需要换一下位置
    # if Swiped.objects.filter(uid = sid).filter(sid = uid).filter(stype__in = ['like','superlike']):
    if Swiped.is_liked(sid, uid):
        # 3.如果双方互相喜欢的话, 匹配成好友
        Friend.make_friends(uid, sid)
        return True
    return False


def dis_someone(uid, sid):
    '''喜欢(右划)某人'''
    # 1. 在数据库中添加滑动记录
    Swiped.objects.update_or_create(uid=uid, sid=sid, stype='like')
    # 2. 检查对方是否右划或者上划过自己
    if Swiped.objects.filter(uid=sid).filter(sid=uid).filter(stype__in=['dislike']):
        # 3.如果双方互相喜欢的话, 匹配成好友
        Friend.make_friends(uid, sid)
        return True
    return False


def dislike_someone(uid, sid):
    # 1. 在数据库中添加滑动记录
    Swiped.objects.update_or_create(uid=uid, sid=sid, stype='dislike')


def super_like_someone(uid, sid):
    '''超级喜欢(右划)某人'''
    # 1. 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='superlike')
    except IntegrityError:
        # 重复滑动时, 直接返回当前用户是否已匹配成好友
        return Friend.is_friends(uid, sid)

    # 2. 检查对方是否右划或者上划过自己
    like_status = Swiped.is_liked(sid,uid)
    if like_status is True:
        # 3.如果双方互相喜欢的话, 匹配成好友
        Friend.make_friends(uid, sid)
        return True
    elif like_status is False:
        return False
    else:
        # 对方未滑动过自己时, 将自己的uid 添加到对方'优先推荐'列表
        key = keys.FIRST_RCMD_Q %sid
        # 从右边推进去
        rds.rpush(key,uid)
        return False
