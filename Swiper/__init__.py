import pymysql

from libs.orm import patch_model

pymysql.install_as_MySQLdb()  # Django 底层用的是 MySQLdb, 需要进行伪装
# Monkey Patch 的方式

# patch_model()  # 为Django 这个model 打补丁, 添加缓存处理
