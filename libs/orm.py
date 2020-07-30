import logging
from datetime import date, datetime
from django.db.models import query
from django.db import models
from common.keys import MODEL_K
from libs.cache import rds

TIMEOUT = 1290600
inf_logger = logging.getLogger('inf')


def get(self, *args, **kwargs):
    """
    Performs the query and returns a single object matching the given
    keyword arguments.
    """
    # 这里的self 是 object 继承过来的 queryset对象
    cls_name = self.model.__name__  # 取出当前model 的名字
    # 检查 kwargs里面有没有主键
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk:
        # 从redis 获取model 对象
        key = MODEL_K % (cls_name, pk)
        model_obj = rds.get(key)
        # 判断当前取出来的对象是不是 model 的一个实例
        if isinstance(model_obj, self.model):
            inf_logger.debug(f'从缓存获取对象: {model_obj}')
            return model_obj

    # 缓存中如果没有取到, 直接从数据库中获取, 这里不要捕获报错
    model_obj = self._get(*args, **kwargs)
    inf_logger.debug(f'从数据库获取对象:{model_obj}')

    # 将取出的model 对象写入缓存
    key = MODEL_K % (cls_name, model_obj.pk)
    rds.set(key, model_obj, TIMEOUT)
    inf_logger.debug('将model对象写入缓存')
    return model_obj


# create 方法底层使用的也是 save方法
def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
    """
    Saves the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    # Ensure that a model instance without a PK hasn't been assigned to
    # a ForeignKey or OneToOneField on this model. If the field is
    # nullable, allowing the save() would result in silent data loss.

    # 先执行 Django 原生save方法将数据保存到 Database
    self._save()

    # 将对象保存到redis
    inf_logger.debug('将model对象写入缓存')
    key = MODEL_K % (self.__class__.__name__, self.pk)
    # 此时需要保存key 和对象本身
    rds.set(key, self, TIMEOUT)  # 缓存两周, 过期即删除


def to_dict(self, exclude=None):
    '''将 Model 对象的属性封装成一个dict'''
    attr_dict = {}
    exclude = exclude or []

    for filed in self._meta.fields:
        name = filed.attname
        if name not in exclude:
            value = getattr(self, name)

            # 这里还需要判断 value 的值类型, 如果是date、datetime 其中的一个的话,
            # 需要转化成 str, 因为只有str可以进行 json的序列化
            # isinstance 里面可以写多个类型
            if isinstance(value, (date, datetime)):
                value = str(value)
            attr_dict[name] = value
    return attr_dict


def patch_model():
    '''通过Monkey Patch 为model 增加缓存处理'''
    query.QuerySet._get = query.QuerySet.get
    query.QuerySet.get = get

    models.Model._save = models.Model.save
    models.Model.save = save

    models.Model.to_dict = to_dict

# 工作中还需要给 filter 和update 、delete 都进行缓存的包装
