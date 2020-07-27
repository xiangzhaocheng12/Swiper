# HIGHEST_PROTOCOL 表示最高的协议 HIGHEST_PROTOCOL = 4,
# 默认的协议版本是 3
from pickle import dumps,loads,HIGHEST_PROTOCOL
from pickle import UnpicklingError
from redis import Redis as _Redis

from Swiper.config import REDIS


class Redis(_Redis):
    '''带 pickle 处理的 Redis 类'''
    def set(self, name, value,
            # ex 表示指定一个过期时间, 单位是 秒
            # px 也表示指定一个过期时间, 单位是 毫秒
            ex=None, px=None, nx=False, xx=False, keepttl=False):
        """
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.

        ``keepttl`` if True, retain the time to live associated with the key.
            (Available since Redis 6.0)
        """

        # 将 value 序列化处理
        pikled_value = dumps(value,HIGHEST_PROTOCOL)
        return super().set(self, pikled_value,ex, px, nx, xx, keepttl)

    def get(self, name,default = None):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        picked_value = super().get(name)

        # 如果picked_value 是空的话,返回默认值
        if picked_value is None:
            return default
        # 如果loads 的值可以直接序列化, 那么
        try:
            return loads(picked_value)
        except UnpicklingError:
            return picked_value

# 全局变量的单例模式, 每次
rds = Redis(**REDIS)