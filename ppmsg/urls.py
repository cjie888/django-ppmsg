from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from ppmsg.views import *
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^inbox/$', inbox, name='messages_inbox'),
    url(r'^outbox/$', outbox, name='messages_outbox'),
    url(r'^compose/$', compose, name='messages_compose'),
    url(r'^compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
    url(r'^search/$', view, name='messages_search'),
    url(r'^reply/(?P<message_id>[\d]+)/$', reply, name='messages_reply'),
    url(r'^view/$', view, name='messages_view'),
    url(r'^detail/(?P<recipient>[\w.@+-]+)/$', view_detail, name='messages_detail'),
    url(r'^delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
    url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
    url(r'^trash/$', trash, name='messages_trash'),
    url(r'^accounts/', include('account.urls')),
    url(r'^code/$', 'toollib.views.home'),
    url(r'^code/captcha/', include('captcha.urls')),
    url(r'code/image/(?P<key>[\w]+)/$','captcha.views.captcha_image',name='verificationcode-image'),
    url(r'code/new/key/$','toollib.verificationcode.code_new_key',name='verificationcode-new-key'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)
