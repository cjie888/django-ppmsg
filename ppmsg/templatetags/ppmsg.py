# -*- coding: utf-8 -*-
from django import template
from django.template import Context

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.tag("compose_msg")
def do_compose_msg(parser, token):
    try:
        tag_name, next = token.split_contents()
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
