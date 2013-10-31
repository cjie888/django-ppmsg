from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from ppmsg.views import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'compose/$', compose, name='messages_compose'),
    url(r'compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'search/$', view, name='messages_search'),
    url(r'view/$', view, name='messages_view'),
    url(r'detail/(?P<username>[\w.@+-]+)/$', view_detail, name='messages_detail'),
    url(r'delete_session/(?P<username>[\w.@+-]+)/$', delete_session, name='messages_delete_session'),
    url(r'set_read/(?P<username>[\w.@+-]+)/$', set_read, name='messages_set_read'),
    url(r'delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
)
