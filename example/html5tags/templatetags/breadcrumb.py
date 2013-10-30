# -*- coding: utf-8 -*-
from django import template
from django.template import Context
from django.core.urlresolvers import reverse

from html5tags.templatetags import CaktNode, parse_args_kwargs


register = template.Library()


@register.tag("breadcrumb")
def do_breadcrumb(parser, token):
    try:
        tag_name, breadcrumb, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % tag_name)
    return BreadcrumbNode(breadcrumb, request)

class BreadcrumbNode(template.Node):
    def __init__(self, breadcrumb, request):
        self.breadcrumb = template.Variable(breadcrumb)
        self.request = template.Variable(request)

    def render(self, context):
        t = template.loader.get_template("breadcrumb.html")
        new_context = Context({'breadcrumb': self.breadcrumb.resolve(context),
                               'request': self.request.resolve(context)}, autoescape=context.autoescape)
        return t.render(new_context)


class AddCrumbNode(CaktNode):
    def render_with_args(self, context, crumb, url=None, *args, **kwargs):
        href = None
        if url:
            if '/' in url:
                href = url
            else:
                href = reverse(url, args=args)
        if 'request' in context:
            if not hasattr(context['request'], 'breadcrumbs'):
                context['request'].breadcrumbs = []
            context['request'].breadcrumbs.append({"name": crumb, "url": href})
        return ''


@register.tag
def add_crumb(parser, token):
    tag_name, args, kwargs = parse_args_kwargs(parser, token)
    return AddCrumbNode(*args, **kwargs)


@register.inclusion_tag('breadcrumb.html', takes_context=True)
def render_breadcrumbs(context):
    if 'request' in context and hasattr(context['request'], 'breadcrumbs'):
        crumbs = context['request'].breadcrumbs
    else:
        crumbs = None
    if crumbs and len(crumbs) == 0:
        crumbs = None
    return {
        'breadcrumb': crumbs,
    }
