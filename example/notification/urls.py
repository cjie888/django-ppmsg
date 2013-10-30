#coding=utf-8


from django.conf.urls import include, url, patterns


urlpatterns = patterns("notification.views",
    url(r"^$", "home"),
    url(r"^(?P<page>\d+)$", "home"),
    url(r"^change/$", "change"),
    url(r"^go/(?P<notice_id>\d+)/$", "go"),
    url(r"^my/$", "my"),
    url(r"^clear/$", "clear"),
)