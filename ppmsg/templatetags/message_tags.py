# -*- coding: utf-8 -*-
from django import template
from django.template import Context
from ppmsg.models import Message, message_count_unread

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.tag("compose_msg")
def do_compose_msg(parser, token):
    try:
        tag_name, next = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % tag_name)
    return ComposeMessageNode(next)


class ComposeMessageNode(template.Node):
    
    def __init__(self, next):
        self._next = template.Variable(next)
        
    def render(self, context):
        t = template.loader.get_template("tags/compose.html")
        next = self._next.resolve(context)
        new_context = Context({'next': next}, autoescape=context.autoescape)
        
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

