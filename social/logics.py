import datetime

from django.db.transaction import atomic

from common import keys
from libs.cache import rds
from social.models import Swiped, Friend
from user.models import Profile, User
# 导入异常
from django.db.utils import IntegrityError


def rcmd_from_queue(uid):
    '''从优先队列里进行推荐'''
    key = keys.FIRST_RCMD_Q % uid
    uid_list = rds.lrange(key, 0, 19)  # 从Redis 取出 优先推荐的用户 ID
    # 这里取出来的都是 bytes 类型的数据, 还需要强转成 int
    uid_list = [int(r_uid) for r_uid in uid_list]  # 将uid 列表元素
    return User.objects.filter(id__in=uid_list)


def rcmd_from_db(uid, num=20):
    '''从数据库获取推荐用户'''
    my_profile = Profile.objects.get(id=uid)
    today = datetime.datetime.today()
    # 注意类型转化:datetime.timedelta !!!
    earliest_date = today - datetime.timedelta(my_profile.max_dating_age * 365)  # 最早出生日期
    lasted_birthday = today - datetime.timedelta(my_profile.min_dating_age * 365)  # 最晚出生日期

    # 需要排除已经划过的人
    # values_list() 用来取出指定的字段, flat  = True 表示
    # 如果不使用 values_list()的话, 会取出所有的
    # select sid from Swiped where uid=1002;
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    # 取出符合条件的用户
    # select * from xx limit 20;
    # select * from xx limit(20,30);
    users = User.objects.filter(
        location=my_profile.dating_location,
        gender=my_profile.dating_gender,
        birthday__gte=earliest_date,
        birthday__lte=lasted_birthday,
        # 排除所有带有滑动记录的 id
    ).exclude(id__in=sid_list)[:num]  # 这里会转化成一个limit 语句

    return users


# 将 上面两个接口整合一下:
def rcmd(uid):
    '''推荐滑动用户'''
    q_users = rcmd_from_queue(uid)  # 从优先推荐队列获取用户
    remain = 20 - len(q_users)
    if remain > 0:  # 如果
        db_users = rcmd_from_db(remain)  # 从数据库获取推荐用户
        return set(q_users) | set(db_users)
    else:  # 如果够了的话, 直接返回队列里面的 q_users
        return q_users


def like_someone(uid, sid):
    '''喜欢(右划)某人'''
    # 1. 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='like')
    # 前端的重复滑动:
    except IntegrityError:
        # 重复滑动时, 直接返回当前用户是否已匹配成好友
        return Friend.is_friends(uid, sid)

    # 强制将对方从自己的优先推荐队列删除
    rds.lrem(keys.FIRST_RCMD_Q % uid, 0, sid)

    # 2. 检查对方是否右划或者上划过自己
    # 这里的uid  和  sid 需要换一下位置
    # if Swiped.objects.filter(uid = sid).filter(sid = uid).filter(stype__in = ['like','superlike']):
    if Swiped.is_liked(sid, uid):
        # 3.如果双方互相喜欢的话, 匹配成好友
        Friend.make_friends(uid, sid)
        return True
    else:
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


def super_like_someone(uid, sid):
    '''超级喜欢(右划)某人'''
    # 1. 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='superlike')
    except IntegrityError:
        # 重复滑动时, 直接返回当前用户是否已匹配成好友
        return Friend.is_friends(uid, sid)

    # 强制将对方从自己的优先推荐队列删除
    rds.lrem(keys.FIRST_RCMD_Q % uid, 0, sid)

    # 2. 检查对方是否右划或者上划过自己
    like_status = Swiped.is_liked(sid, uid)
    if like_status is True:
        # 3.如果双方互相喜欢的话, 匹配成好友
        Friend.make_friends(uid, sid)
        return True
    elif like_status is False:
        return False
    else:
        # 对方未滑动过自己时, 将自己的uid 添加到对方'优先推荐'列表
        key = keys.FIRST_RCMD_Q % sid
        # 从右边推进去
        rds.rpush(key, uid)
        return False


def dislike_someone(uid, sid):
    '''不喜欢(左划)某人'''
    # 1. 在数据库中添加滑动记录
    try:
        Swiped.objects.create(uid=uid, sid=sid, stype='dislike')
    except IntegrityError:
        pass

    # 强制将对方从自己的优先推荐队列删除
    rds.lrem(keys.FIRST_RCMD_Q % uid, 0, sid)


def find_fans(uid):
    '''
    查找自己的粉丝, 自己尚未划过, 但是对方喜欢过自己的人
    :param uid:
    :return:
    '''
    # 取出已划过的用户 ID 列表
    sid_list = Swiped.objects.filter(uid=uid).values_list('sid', flat=True)

    like_types = ['like', 'superlike']
    fans_id_list = \
        Swiped.objects.filter(sid=uid, stype__in=like_types). \
            exclude(uid__in=sid_list). \
            values_list('uid', flat=True)  # 然后取出对方的id
    return User.objects.filter(id__in=fans_id_list)


def rewind_last_swipe(uid):
    '''
    反悔最后一次滑动的记录(确定逻辑顺序):
    :param uid: 用户的 ID
    :return:
    '''
    # 1.检查今天是否已经达到3次
    #   还需要拼接一个时间, 确保删除的次数是当天的
    now = datetime.datetime.now()
    key = 'Rewind-%s-%s' % (uid, now.date())
    # 取出当天反悔的次数, 默认为0
    rewind_times = rds.get(key, 0)
    if rewind_times >= 3:
        print('反悔次数达到限制')
        return 1007  # TODO: 需要给前端反回状态码

    # 2.从数据库里面取出最后一次滑动的记录
    latest_swiped = Swiped.objects.filter(uid=uid).latest('stime')

    # 3.检查反悔记录是否是五分钟以内的
    past_time = now - latest_swiped.stime
    if past_time.seconds > 300:
        print('反悔超时')
        return 1008  # TODO: 需要给前端反回状态码

    # 给下面操作数据库的代码添加事务:
    with atomic():
        # 4.检查上次滑动记录是否匹配成功, 如果匹配成功的话, 需要删除好友
        #       不管之前有没有, 都来一次删除, 强删的话是不会报错的
        if latest_swiped.stype in ['like','superlike']:
            Friend.break_off(uid,latest_swiped.sid)

        # 5.检查上次是否是超级喜欢, 如果是, 将自己的ID从对方的优先队列中删除
        if latest_swiped.stype == 'superlike':
            # 把对方优先队列中自己的记录给删除
            rds.lrem(keys.FIRST_RCMD_Q %latest_swiped.sid,0,uid)
        # 6.删除滑动记录
        latest_swiped.delete()

        # 7. 累加当天反悔次数
        rds.set(key,rewind_times + 1)
