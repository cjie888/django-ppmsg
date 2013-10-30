# -*- coding:utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape


__all__ = ('BaseForm', 'Form',)


class BaseForm(forms.BaseForm):
    def as_bootstrap(self):
        "Returns this form rendered as bootstrap style."
        return self._html_output(
            normal_row = u'<div class="form-group"%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</div>',
            error_row = u'<label>%s</label>',
            row_ender = '</div>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False)


@python_2_unicode_compatible
class BootstrapErrorList(ErrorList):
    def as_ul(self):
        if not self: return u''
        return mark_safe(u'<ul class="errorlist">%s</ul>'
                % ''.join([u'<li><small><font color="#ff0000">%s</font></small></li>' %
                           conditional_escape(force_unicode(e)) for e in self]))


    def __str__(self):
        return self.as_ul()


class Form(BaseForm, forms.Form):
    def __init__(self, *args, **kwargs):
        new_kwargs = {'error_class': BootstrapErrorList}
        new_kwargs.update(kwargs)
        super(Form, self).__init__(*args, **new_kwargs)
