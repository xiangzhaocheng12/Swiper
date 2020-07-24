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
    def process_request(self,request):
        # 检查当前接口是否在白名单中
        if request.path in self.white_list:
            return
        uid = request.session.get('uid')
        if uid is None:
            return render_json(code = stat.LOGIN_REQUIRED)
        else:
            # 直接把  uid 绑定到request上面
            # 后面就不需要通过 session来进行获取了
            request.uid = uid

