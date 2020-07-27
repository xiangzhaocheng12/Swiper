from django.db import models


# Create your models here.
from django.db.models import Q
from user.models import User


class Swiped(models.Model):
    '''滑动记录'''
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动者的UID')
    sid = models.IntegerField(verbose_name='被滑动者的UID')
    stype = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    # auto_now: 每次操作的时候, 自动修改时间
    # auto_now_add:创建的时间修改时间
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    # 联合唯一
    class Meta:
        unique_together = ('uid', 'sid')  #

    @classmethod
    def is_liked(cls,uid,sid):
        '''检查是否喜欢过某人'''
        stypes = ['like','superlike']
        try:
            # 查看自己是不是划过对方
            swipe_record = cls.objects.get(uid = uid,sid = sid)
        except cls.DoesNotExist:
            return None     # 表示还没有滑动过对方
        else:
            # 喜欢返回True, 不喜欢返回False
            return swipe_record.stype in stypes   # 为 True, 说明喜欢过, 为 False  说明不喜欢




class Friend(models.Model):
    # 通过程序本身, ID 小的为第一条字段, ID大的放在后面
    #
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    class Meta:
        unique_together = ('uid1', 'uid2')  # uid1 和 uid2 联合唯一

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''建立好友关系'''
        # 排序法1:
        # uid1,uid2 = (uid2,uid1) if uid1 > uid2 else (uid1,uid2)
        # 排序法2:
        uid1, uid2 = sorted([uid1, uid2])  # 将uid 小的放在前面
        # 存在的话获取,不存在就创建一个
        frd_relation,if_created = cls.objects.get_or_create(uid1=uid1, uid2=uid2)
        return if_created

    # 检查是否是你的好友, 用作重复滑动时返回是否有好友这条记录
    @classmethod
    def is_friends(cls, uid1,uid2):
        '''检查两个人是否时好友'''
        uid1, uid2 = sorted([uid1, uid2])  # 将uid 小的放在前面
        # 是否存在
        return cls.objects.filter(uid1=uid1,uid2 = uid2).exists()

    # 查看好友的接口
    @classmethod
    def my_friends(cls,uid):
        '''我所有好友 ID 列表'''
        frd_id_list = []
        condition = Q(uid1 = uid) | Q(uid2 = uid)

        for frd in cls.objects.filter(condition):
            if frd.uid1 == uid:
                frd_id_list.append(frd.uid2)
            else:
                frd_id_list.append(frd.uid1)
        return User.objects.filter(id__in = frd_id_list)

    @classmethod
    def break_off(cls,uid1,uid2):
        # 还是要先排序
        uid1, uid2 = sorted([uid1, uid2])
        cls.objects.filter(uid1 = uid1, uid2 = uid2).delete()