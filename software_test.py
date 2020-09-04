import unittest


def div(a, b):
    return a / b


class DivTest(unittest.TestCase):
    '''除法的测试用例'''

    def test_int(self):
        '''测试整形数值'''
        result = div(15, 3)
        # 断言 是 5.0
        self.assertEqual(result, 5.0)
        self.assertIsInstance(result, float)

        result = div(-36, 12)
        self.assertEqual(result, -3.0)
        self.assertIsInstance(result, float)

    def test_float(self):
        '''测试浮点型数值'''
        result = div(21.45, 3)
        # 断言 是 5.0
        # python 中的除法无法进行真正的除法
        # 因此需要进行 round() 进行近似的操作
        self.assertIsInstance(result, float)
        self.assertEqual(round(result,5), 7.15)

    def test_loop_float(self):
        '''测试无限循环小数'''
        result = div(7, 3)
        # assertAlmostEqual: 约等于
        self.assertAlmostEqual(result, 2.33333, delta=0.0000001)

    def test_zero(self):
        '''测试零值'''
        # 0 作被除数
        result = div(0, 1234567)
        self.assertEqual(result,0.0)
        # 0 作除数
        # 抛出一个异常,
        # 不管有没有异常,with 语句都能捕获
        # with 语句即使报错了也会正常执行完毕
        with self.assertRaises(ZeroDivisionError):
            result = div(123212,0)

    def test_other_types(self):
        '''测试其它列表'''
        data = [
            [1,2,3,4],
            {5,6,7,8},
            {1:11,2:22,3:33}
        ]
        for x in data:
            with self.assertRaises(TypeError):
                result = div(x, 3)

if __name__ == '__main__':
    # 自动检索测试用例
    unittest.main()
