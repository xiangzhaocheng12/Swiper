from django.conf.urls import url

from user import api

urlpatterns = [
    url(r'^vcode/fetch', api.fetch, name='fetch'),
    url(r'^vcode/submit', api.submit, name='submit')
]
