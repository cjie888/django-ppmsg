#coding=utf-8

from django.utils.safestring import mark_safe
from models import NoticeList
from table import Table
from table.columns import Column
from notification import config

class NewTable(Table):
    def render_ext_button(self):
        html = ''
        if self.opts.ext_button_link:
            html = '<a href="%s"  class="btn btn-default">%s</a>' % \
                (self.opts.ext_button_link, self.opts.ext_button_text)
        return mark_safe(html)


class NoticeTable(NewTable):
    add_datetime = Column(field='add_datetime', header=u'日期', header_attrs={'width': '20%'})
    content = Column(field='content', safe=False,  header=u'通知', header_attrs={'width': '80%'})
    class Meta:
        model = NoticeList
        #ext_button_link = reverse("notification.views.show_unread")
        ext_button_link = config.UNREAD_URL
        ext_button_text = u"显示未读通知"


class UnreadNoticeTable(NewTable):
    add_datetime = Column(field='add_datetime', header=u'日期', header_attrs={'width': '20%'})
    content = Column(field='content', safe=False,  header=u'通知', header_attrs={'width': '80%'})

    class Meta:
        model = NoticeList
        #ext_button_link =  reverse("notification.views.home")
        ext_button_link = config.ALL_NOTICES_URL
        ext_button_text = u"显示全部通知"