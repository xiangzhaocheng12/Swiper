
# 在独立的脚本中调用Django模块
import os
import sys
import django

# 1. 先设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Swiper.settings")
# 2. 找到当前项目的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 3. 将django的环境变量添加到主环境变量
sys.path.insert(0,BASE_DIR)
# 4. 此时进行运行会抛出 模块未被加载的异常: 需要进行setup()
django.setup()

from user.models import User