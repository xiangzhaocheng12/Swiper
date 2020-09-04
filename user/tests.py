import json
import sys
import os

from django.test import TestCase
from django.conf import settings

# 首先要把这些测试数据都给创建出来, 用来当作测试的数据集
script_dir = os.path.join(settings.BASE_DIR,'script')
sys.path.append(script_dir)

from scripts.data_init import create_robots
from scripts.data_init import create_vip_data
from libs.cache import rds
from common.keys import VCODE_K
from user.models import User

class UserTestCase(TestCase):
    def setUp(self):
        # super(UserTestCase, self).setUp()
        super().setUp()
        # 需要重新生成数据用于测试
        create_robots(1000)
        create_vip_data()
        rds.set(VCODE_K %'15601185621','123456')
        user = User.objects.create(id = 1001, nickname = 'Seamile',phonenum='15601185621')

    def test_login(self):
        response = self.client.post('/api/user/vcode/submit',
                                    {'phonenum':'15601185621','vcode':'123456'})
        self.assertEqual(response.status_code, 200)
        # content 是一个 json 数据
        result = json.loads(response.content)
        # 一般使用 get 来获取指定键的值
        self.assertEqual(result.get('data',{}).get('id'),1001)
        self.assertEqual(result.get('data',{}).get('phonenum'),'15601185621')

    def test_like(self):
        self.client.post('/api/user/vcode/submit',
                                    {'phonenum':'15601185621','vcode':'123456'})

        response = self.client.post('/api/social/like',data={'sid':'100'})
        self.assertEqual(response.status_code,200)
        result = json.loads(response.content)
        self.assertEqual(result.get('code'),0)

