from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from ppmsg.views import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^msg/compose/$', compose, name='messages_compose'),
    url(r'^msg/compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'^msg/search/$', view, name='messages_search'),
    url(r'^msg/view/$', view, name='messages_view'),
    url(r'^msg/detail/(?P<username>[\w.@+-]+)/$', view_detail, name='messages_detail'),
    url(r'^msg/delete_session/(?P<username>[\w.@+-]+)/$', delete_session, name='messages_delete_session'),
    url(r'^msg/set_read/(?P<username>[\w.@+-]+)/$', set_read, name='messages_set_read'),
    url(r'^msg/delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
    url(r'^accounts/', include('account.urls')),
    url(r'notification/', include('notification.urls')),
    url(r'^code/$', 'toollib.views.home'),
    url(r'^code/captcha/', include('captcha.urls')),
    url(r'code/image/(?P<key>[\w]+)/$','captcha.views.captcha_image',name='verificationcode-image'),
    url(r'code/new/key/$','toollib.verificationcode.code_new_key',name='verificationcode-new-key'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)
