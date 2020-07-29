from common.stat import PermErr
from user.models import User

def require_perm(perm_nmae):
    def deco(view_func):
        def wrapper(request, *args,**kwargs):
            user = User.objects.get(id = request.uid)
            # 检查是否有权限, 有的话 返回 response,没有的话返回异常
            if user.vip.has_perm(perm_nmae):
                response = view_func(request, *args, **kwargs)
                return response
            else:
                return PermErr
        return wrapper
    return deco