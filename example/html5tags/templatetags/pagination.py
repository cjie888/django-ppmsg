# -*- coding: utf-8 -*-
from django import template
from django.template import Context

register = template.Library()


@register.tag("pagination")
def do_pagination(parser, token):
    try:
        tag_name, pager, prefix, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two argument" % token.contents.split()[0])

    if prefix[0] != prefix[-1] and prefix[0] in ('"', "'"):
        raise template.TemplateSyntaxError("%r tag's second argument should be in quotes" % tag_name)
    return PaginationNode(pager, prefix, request)


class PaginationNode(template.Node):
    def __init__(self, pager, prefix, request):
        self._pager = template.Variable(pager)
        self._prefix = template.Variable(prefix)
        self._request = template.Variable(request)

    def render(self, context):
        t = template.loader.get_template("pagination.html")
        url = self._prefix.resolve(context)
        request = self._request.resolve(context)
        pager = self._pager.resolve(context)

        if "?" in url:
            prefix = url.split("?")[0]
            parameter = url.split("?")[1]
            new_context = Context({"pager": pager, "request": request,
                                   "prefix": prefix, "parameter": parameter},
                                  autoescape=context.autoescape)
        else:
            new_context = Context({"pager": pager, "request": request,
                                   "prefix": url},
                                  autoescape=context.autoescape)
        return t.render(new_context)
