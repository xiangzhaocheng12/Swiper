from django.conf.urls import url

from qiNiu import api

urlpatterns = [
    url(r'^token/', view=api.token, name='token')
]
