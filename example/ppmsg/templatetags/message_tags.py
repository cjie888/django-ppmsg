# -*- coding: utf-8 -*-
from django import template
from django.template import Context
from django.core.urlresolvers import reverse

from ppmsg.models import Message, message_count_unread

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.tag("compose_msg")
def do_compose_msg(parser, token):
    try:
        params = token.contents.split()
        next_page = reverse('messages_view')
        if (len(params)) > 1:
            tag_name = params[0]
            next_page = params[1]
        else:
            tag_name = params[0]

    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % tag_name)
    return ComposeMessageNode(next_page)


class ComposeMessageNode(template.Node):
    
    def __init__(self, next_page):
        self._next_page = template.Variable(next_page)
        
    def render(self, context):
        t = template.loader.get_template("tags/compose.html")
        next_page = self._next_page.resolve(context)
        new_context = Context({'next_page': next_page}, autoescape=context.autoescape)
        
        return t.render(new_context)

@register.tag("messages")
def do_get_message_list(parser, token):
    """
    Get private messages for a given object

    Example usage:
        {%  messages user %}
    """

    try:
        tag_name, request = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % tag_name)
    return GetMessagesNode(request)

class GetMessagesNode(template.Node):
    def __init__(self, request):
        self._request = template.Variable(request)

    def render(self, context):
        request = self._request.resolve(context)
        message_list = Message.objects.messages_all(request.user)
        t = template.loader.get_template("tags/messages.html")
        user_lastmsgs = {}
        for message in message_list:
            if message.sender not in user_lastmsgs and message.sender != request.user:
                user_lastmsgs[message.sender] = message
            if message.recipient not in user_lastmsgs and message.recipient != request.user:
                user_lastmsgs[message.recipient] = message
        msg_unreads = {}
        for user in user_lastmsgs:
            msg_unreads[user] = message_count_unread(user, request.user)
        new_context = Context({'users': user_lastmsgs, 'unreads' : msg_unreads},
                               autoescape=context.autoescape)
        return t.render(new_context)

