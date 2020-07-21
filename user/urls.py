from django.conf.urls import url

from user import api

urlpatterns = [
    url(r'^vcode/fetch', api.sub_phnum,name='fetch'),
]
