# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('account.views',
    url(r'^register/$', "register"),
    url(r'^login/$', 'login'),
    url(r"^logout/$", "logout"),
    url(r'^change_password/$', 'change_password'),
    url(r'^home/$', 'home'),
    url(r'prepare_reset_password/', 'prepare_reset_password'),
    url(r'reset_password/(?P<userid>[0-9A-Za-z]+)-(?P<token>.+)/', 'reset_password'),
    url(r'change_user_icon/', 'change_user_icon'),
)
