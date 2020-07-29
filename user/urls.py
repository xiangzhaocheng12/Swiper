from django.conf.urls import url

from user import apis

urlpatterns = [
    url(r'^vcode/fetch', apis.fetch, name='fetch'),
    url(r'^vcode/submit', apis.submit, name='submit'),
    url(r'^profile/show', apis.show, name='show'),
    url(r'^profile/update', apis.update, name='update'),
]
