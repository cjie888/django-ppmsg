from django.conf.urls import patterns, include, url
import settings

urlpatterns = patterns('',
    url(r'^msg/', include('ppmsg.urls')),
    url(r'^accounts/', include('account.urls')),
    url(r'notification/', include('notification.urls')),
    url(r'^code/$', 'toollib.views.home'),
    url(r'^code/captcha/', include('captcha.urls')),
    url(r'code/image/(?P<key>[\w]+)/$','captcha.views.captcha_image',name='verificationcode-image'),
    url(r'code/new/key/$','toollib.verificationcode.code_new_key',name='verificationcode-new-key'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
)
