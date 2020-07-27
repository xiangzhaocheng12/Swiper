from libs.cache import rds
# 这个是自己写的 render返回函数, 用来代替原先的JsonResponse()
from Swiper import config
from libs import qn_cloud
from libs.http_ import render_json
from common import keys
from user import logics
from user.forms import UserForm
from user.forms import ProfileForm
from user.models import User
from user.models import Profile
from common import stat

# 客户端 -> 服务器
#                   -> 短息平台 -> 运营商    过程很长, 需要进行等待, 对于用户不友好
# 此时应该使用 Celery 异步任务处理框架
# celery worker -A task_test(celery文件的名字) --loglevel=INFO  启动celery 的命令
def fetch(request):
    """ 提交手机号 """
    # GET 是一个字典类型
    phonenum = request.GET.get('phonenum')
    # 检查用户手机号是否正确
    if logics.is_phonenum(phonenum):
        # 如果手机号正确的话, 发送验证码, 判断是否发送成功
        # 异步发送
        # 此时if 判断不判断已经不重要了, 直接返回正确结果,
        # if logics.send_vcode.delay(phonenum):
        logics.send_vcode.delay(phonenum)
        return render_json()
    # 如果手机号验证失败的话, 直接返回验证码发送失败
    return render_json(code=stat.SEND_FAILD)


def submit(request):
    """提交验证码, 完成登陆、注册"""
    # strip() 用来取出字符串两端空格
    phonenum = request.POST.get('phonenum', '').strip()
    vcode = request.POST.get('vcode', '').strip()

    # 从缓存获取验证码
    key = keys.VCODE_K % phonenum
    cached_vcode = rds.get(key)

    # 检查验证码
    # vcode: 用户提交的验证码,     cached_vcode: 缓存中的验证码
    # 需要考虑下面这种情况:
    #       None == None
    if True:#vcode and vcode == cached_vcode:
        # 根据手机号获取用户
        # flask 里面不是 objects, 而是一个query
        #   User.query.filter(...).one()
        # get:只能获取一个
        try:
            user = User.objects.get(phonenum=phonenum)
        # 这里不能只写一个except, 需要精确的写上一个异常
        except User.DoesNotExist:
            # user = User()
            # ....
            # user.save()
            # 法2：
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)

        # 通过 Session 记录用户登陆状态
        # session 保存在服务器的什么位置: Django默认保存在数据库中, 配置在settings中的INSTALLED_APPS中
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return render_json(code=stat.VCODE_ERR)


def show(request):
    """获取用户交友信息"""
    uid = request.session.get('uid')
    # 直接用 id进行关联
    profile, _ = Profile.objects.get_or_create(id=uid)
    return render_json(data=profile.to_dict())


def update(request):
    '''修改资料'''
    # 从request.POST 里面得到一个类字典的对象
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)
    # 如果两个提交的信息都没有问题的话:
    if user_form.is_valid() and profile_form.is_valid():

        uid = request.session['uid']
        # update `user` set nickname = 'xxx' ... where id = 123;

        # UserForm.cleaned_data 是更新的数据, 并且需要进行拆包, 因为这个是一个字典
        User.objects.filter(id=uid).update(**user_form.cleaned_data)

        # 先更新, 如果没有数据可供更新的话, 创建一个新的并将 default 作为默认的写进去
        Profile.objects.update_or_create(id=uid, defaults=profile_form.cleaned_data)
        return render_json()
    # 如果有异常的话:
    else:
        # 错误信息是用字典来标记的
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        return render_json(err, stat.PROFILE_ERR)


def qn_token(request):
    '''获取头像上传凭证'''
    # 中间件里面已经设置了 request.uid = uid 了
    # 这个是用户访问的, 用户访问之后返回一个 token
    # 增加一个 Avatar, 用来表示头像, 为了将该用户账户上的头像和别的用户相区别
    key = 'Avatar-%s' % request.uid  # 上传后的文件名
    token = qn_cloud.get_token(request.uid,key)
    return render_json({'key': key, 'token': token})


def qn_callback(request):
    '''七牛云回调'''
    # 七牛云进行访问
    uid = request.POST.get('uid')
    key = request.POST.get('key')
    avatar_url = '%s/%s' % (config.QN_HOST,key)
    # 修改用户的头像地址
    # 为什么这里需要用filter, 不能使用get来进行获取
    # AttributeError: 'User' object has no attribute 'update'
    # 法1：  使用 filter  对多个进行更改
    # user = User.objects.filter(id = uid).update(avatar = avatar_url)
    # 法2：  使用 get 对一个进行更改该
    user = User.objects.get(id = uid)
    user.avatar = avatar_url
    user.save()
    print(User.objects.filter(id = uid))
    return render_json(data = avatar_url)
