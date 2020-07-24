"""Swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

import user
from home import views
from user.api import qn_token

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$',views.home),
    url(r'^api/user/', include('user.urls',namespace='user')),
    url(r'^qiniu/token/', user.api.qn_token),
    url(r'^qiniu/callback',user.api.qn_callback),
]
