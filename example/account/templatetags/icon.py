# -*- coding: utf-8 -*-
from django import template
from django.template import Context
from account.views import get_user_icon
from settings import MEDIA_URL

register = template.Library()


@register.tag("usericon")
def do_usericon(parser, token):
    try:
        tag_name, user, size, link = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % tag_name)

    return UsericonNode(user, size, link)


class UsericonNode(template.Node):
    def __init__(self, user, size, link):
        self._user = template.Variable(user)
        self._size = template.Variable(size)
        self._link = template.Variable(link)

    def render(self, context):
        t = template.loader.get_template("tags/usericon.html")
        user = self._user.resolve(context)
        size = self._size.resolve(context)
        link = self._link.resolve(context)
        icon = get_user_icon(user)
        
        new_context = Context({"user": user, "size": size, "icon": icon, "link": link, "MEDIA_URL": MEDIA_URL},
                              autoescape=context.autoescape)

        return t.render(new_context)
