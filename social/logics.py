import datetime

from user.models import Profile, User


def rcmd(uid):
    '''推荐滑动用户'''
    my_profile = Profile.objects.get(id=uid)
    today = datetime.datetime.today()
    # 注意类型转化:datetime.timedelta !!!
    earliest_date = today - datetime.timedelta(my_profile.max_dating_age * 365)  # 最早出生日期
    lasted_birthday = today - datetime.timedelta(my_profile.min_dating_age * 365)  # 最晚出生日期

    # 取出符合条件的用户
    # select * from xx limit 20;
    # select * from xx limit(20,30);
    users = User.objects.filter(
        location=my_profile.dating_location,
        gender=my_profile.dating_gender,
        birthday__gte=earliest_date,
        birthday__lte=lasted_birthday,
    )[:20]  # 这里会转化成一个limit 语句

    # TODO: 需要排除已经划过的人

    return users


def like_someone(uid, sid):
    '''喜欢(右划)某人'''
    # 1. 在数据库中添加滑动记录
    # 2. 检查对方是否右划或者上划过自己
    # 3.如果双方互相喜欢的话, 匹配成好友

