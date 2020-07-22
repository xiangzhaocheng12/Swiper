from django.db import models


# Create your models here.
class User(models.Model):
    GENDERS = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATIONS = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('武汉', '武汉'),
        ('成都', '成都'),
    )
    # phonenum 需要加上unique
    # unique 在 Mysql 中保证唯一性使用的唯一索引, 因此这个字段也是一个索引
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    # nickname 使用索引: B-tree, O(log_2n)
    nickname = models.CharField(max_length=20, db_index=True, verbose_name='昵称')
    # 枚举   enum()
    # 但是Django里面没有枚举的类型, 因此需要使用Django自带的限制方式, 使用choice 参数
    gender = models.CharField(max_length=10, default='male', choices=GENDERS, verbose_name='性别')
    # 使用Date类型(因为不需要时分秒)
    birthday = models.DateField(default='2000-01-01', verbose_name='出生日')
    # ImageField 保存的是文件路径, 这里保存的是一个网址的路径
    avatar = models.CharField(max_length=256, verbose_name='个人形象 URL')
    location = models.CharField(max_length=10, choices=LOCATIONS, default='上海', verbose_name='常居地')

# 各种的 int 大小
# tiny int    1 字节    8个二进制位     最大可以存储2^8 = 255
# small int   4 字节    32个二进制位    最大可以存储2^32 =


# Mysql 也是可以保存二进制的数据: blob数据类型, 但是不建议使用
    def to_dict(self):
        return {
        'phonenum' : self.phonenum,
        'nickname' : self.nickname,
        'gender' : self.gender,
        'birthday' : self.birthday,
        'avatar' : self.avatar,
        'location' : self.location,
        }
