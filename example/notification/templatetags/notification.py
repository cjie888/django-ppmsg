#coding=utf-8
""" notification template tags
"""

from django import template
from django.template import Context
from django.core.urlresolvers import reverse
from settings import DISAPPEAR_INTERVAL_TIMESTAMP


register = template.Library()

@register.tag("notification_list")
def do_notification_list(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, notifications, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % token.contents.split()[0]) 
    return NotificationListNode(notifications, request)


class NotificationListNode(template.Node):
    def __init__(self, notifications, request): 
        self.notifications = template.Variable(notifications)
        self.request = template.Variable(request)
        
    def render(self, context):
        t = template.loader.get_template("notification/tags/list.html")
        new_context = Context({"notifications": self.notifications.resolve(context), 
                               "request": self.request.resolve(context)}, 
                              autoescape=context.autoescape)
        return t.render(new_context)
    
    
@register.tag("notice")
def do_notice(parser, token):
    try:
        tag_name, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % tag_name)
    return NoticeNode(request)


class NoticeNode(template.Node):
    def __init__(self, request):
        self.request = template.Variable(request)

    def render(self, context):
        request = self.request.resolve(context)
        t = template.loader.get_template("notification/tags/notice.html")
        new_context = Context({"request": request, "disappear_interval_timestamp": DISAPPEAR_INTERVAL_TIMESTAMP}, autoescape=context.autoescape)
        return t.render(new_context)

