import os

from celery import Celery
from tasks import config

celery_app = Celery('task')
# 从一个对象里面加载配置
celery_app.config_from_object(config)


# 此时celery还是一个独立的模块, 类似manage.py 里面的os.environ.setdefault(...)
# 首先加载这个环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Swiper.settings")
# 然后加载啥啥来着的
celery_app.autodiscover_tasks()