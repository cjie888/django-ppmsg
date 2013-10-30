#coding=utf-8
  
# from html5helper.forms import BasisForm
# from html5helper.fields import ChoiceField
# from html5helper.widgets import InlineCheckboxSelectMultiple
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe
from notification.models import NoticeSetting
import html5tags.bootstrap as NewForms


class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return u""
        return u'<div class="alert">%s</div>' % ''.join([u'<div class="alert-error">%s</div>' % e for e in self])

    def as_ul(self):
        return self.as_divs()


class BasisForm(NewForms.Form):
    """ basis form class.
    """
    _custom_error = ""
    _success_tips = ""

    @property
    def custom_error(self):
        if self._custom_error == "":
            return ""
        return mark_safe(u"<div class=\"alert\">%s</div>" % self._custom_error)

    def set_custom_error(self, msg):
        self._custom_error = msg

    @property
    def success_tips(self):
        if self._success_tips == "":
            return ""
        return mark_safe(u"<div class=\"alert alert-success\">%s</div>" % self._success_tips)

    def set_success_tips(self, tips):
        self._success_tips = tips


class NoticeSettingForm(BasisForm):

#     pre_notify_days = NewForms.IntegerField(label=u"提前几天通知", help_text=u"提前通知时间", required=False)

    def __init__(self, *args, **kwargs):
        """ must have "user" as args
        """
        self.user = None
        if "user" in kwargs:
            self.user = kwargs.pop("user")
         
        super(NoticeSettingForm, self).__init__(*args, **kwargs)
        notice_settings = NoticeSetting.objects.myself(self.user)
        for notice_setting in notice_settings:
            self.fields[notice_setting.notice_type.label] = NewForms.MultipleChoiceField(label=notice_setting.notice_type.display,
                                                                         help_text=notice_setting.notice_type.description,
                                                                         widget=NewForms.CheckboxSelectMultiple(), 
                                                                         choices=NoticeSetting.DEVICE_CHOICES, 
                                                                         required=False)
