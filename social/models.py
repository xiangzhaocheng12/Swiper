from django.db import models


# Create your models here.

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