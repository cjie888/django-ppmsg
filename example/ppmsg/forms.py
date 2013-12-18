# -*- coding: UTF-8 -*-
import datetime
from django import forms
from django.utils.translation import ugettext_lazy as _
from html5tags.bootstrap import fields
from ppmsg.models import Message
from ppmsg.fields import CommaSeparatedUserField

class ComposeForm(forms.Form):
    """
    A simple default form for private messages.
    """
    #recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    recipient = CommaSeparatedUserField(label=_(u"发给"), widget=forms.TextInput(attrs={'placeholder':'输入用户名，多个用户名用逗号分隔'}))
    content = fields.CharField(label=_(u"内容"), max_length=300, widget=forms.Textarea(attrs={'rows':3, 'placeholder':'私信内容'}))
        
    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter
    
                
    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        content = self.cleaned_data['content']
        message_list = []
        for r in recipients:
            msg = Message(
                sender = sender,
                recipient = r,
                content = content,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.replied_at = datetime.datetime.now()
                parent_msg.save()
            msg.save()
            message_list.append(msg)
        return message_list
