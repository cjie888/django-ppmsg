#coding=utf-8

from models import NoticeList
from table import Table
from table.columns import Column

class NoticeTable(Table):
    add_datetime = Column(field='add_datetime', header=u'日期', header_attrs={'width': '20%'})
    content = Column(field='content', safe=False,  header=u'通知', header_attrs={'width': '80%'})

    class Meta:
        model = NoticeList