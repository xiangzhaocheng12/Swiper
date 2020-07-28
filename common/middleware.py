from django.utils.deprecation import MiddlewareMixin

from libs.http_ import render_json
from common import stat


class AuthMiddleware(MiddlewareMixin):
    '''登陆中间件'''
    # 不是所有的接口都是需要进行登陆验证的, 因此需要建立白名单
    white_list = [
        '/',
        '/api/user/vcode/fetch',
        '/api/user/vcode/submit',
        '/qiniu/callback',
        '/qiniu/'
    ]

    def process_request(self, request):
        # 检查当前接口是否在白名单中
        if request.path in self.white_list:
            return
        uid = request.session.get('uid')
        if uid is None:
            # 这个code是啥
            return render_json(code=stat.LoginRequired.code)
        else:
            # 直接把  uid 绑定到request上面
            # 后面就不需要通过 session来进行获取了
            request.uid = uid


class LogicErrMiddleware(MiddlewareMixin):
    '''逻辑异常处理中间件'''

    # 这个err 是一个对象的实例   类似于 except ValueError as e 当中的 e
    # Django 本身里面有一个try, process_exception 已经在这个try 里面了
    def process_exception(self, request, err):
        # 此时必须是逻辑异常的时候, 才进行处理, 如果是别的异常, 不去做处理
        if isinstance(err, stat.LogicErr):
            # 反回的data 是错误信息的类
            return render_json(err.data, code=err.code)

# try:
#     LogicErrMiddleware()
#     # e 是这个的一个实例
# except ValueError as e:
#     print(e)
