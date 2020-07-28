OK = 0
class LogicErr(Exception):
    code = OK
    data = None

    def __init__(self, err_data=None):
        # 先执行一下父类的 __init__
        super().__init__()

        # 利用魔法属性获取到类的名字
        # 通过实例.__class__获取自身的类, 然后通过__name__ 获取类的名字
        # 通过中间件把这个类的名字反回到前端
        self.data = err_data or self.__class__.__name__

# 这里使用元类的方式
# 使用元类定义多个状态码的类
def gen_logic_err(name, code):
    '''生成一个新的 LogicErr 子类'''
    return type(name, (LogicErr,), {'code': code})


SendFaild = gen_logic_err('SendFaild', 1000)          # 验证码发送失败
VcodeErr = gen_logic_err('VcodeErr', 1001)            # 验证码错误
LoginRequired = gen_logic_err('LoginRequired', 1002)  # 需要⽤户登陆
ProfileErr = gen_logic_err('ProfileErr', 1003)        # ⽤户资料表单数据错误
SidErr = gen_logic_err('SidErr', 1004)                # SID 错误
StypeErr = gen_logic_err('StypeErr', 1005)            # 滑动类型错误
SwipeRepeat = gen_logic_err('SwipeRepeat', 1006)      # 重复滑动
RewindLimited = gen_logic_err('RewindLimited', 1007)  # 反悔次数达到限制
RewindTimeout = gen_logic_err('RewindTimeout', 1008)  # 反悔超时
NoSwipe = gen_logic_err('NoSwipe', 1009)              # 当前还没有滑动记录
PermErr = gen_logic_err('PermErr', 1010)              # ⽤户不具有某权限
