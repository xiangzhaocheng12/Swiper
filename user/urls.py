from django.conf.urls import url

from user import api

urlpatterns = [
    url(r'^vcode/fetch', api.fetch, name='fetch'),
    url(r'^vcode/submit', api.submit, name='submit'),
    url(r'^profile/show', api.show, name='show'),
    url(r'^profile/update', api.update, name='update'),
    url(r'^token/',api.qn_token)
]
