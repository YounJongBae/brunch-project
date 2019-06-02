from django.conf.urls import url, include
from django.contrib import admin
from .views import (
        index, detail, signup, common_signup, login, logout, signup_cong, userpage, write
    )

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<article_id>[0-9]+)/$', detail, name='detail'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^signup_cong/$', signup_cong, name='signup_cong'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^write/$', write, name='write'),
    url(r'^@(?P<username>\w+)/$', userpage, name='userpage'),
]
