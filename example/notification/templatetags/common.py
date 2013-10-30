# -*- coding: utf-8 -*-
from django import template
from django.template import Context
from django.core.urlresolvers import reverse


register = template.Library()


@register.tag("form_html")
def do_form_html(parser, token):
    try:
        tag_name, form, btn_text, form_url = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % tag_name)
    return FormHtmlNode(form, btn_text, form_url)


class FormHtmlNode(template.Node):
    def __init__(self, form, btn_text, form_url):
        self.form = template.Variable(form)
        self.btn_text = template.Variable(btn_text)
        self.form_url = template.Variable(form_url)

    def render(self, context):
        form = self.form.resolve(context)
        btn_text = self.btn_text.resolve(context)
        form_url = self.form_url.resolve(context)
        t = template.loader.get_template("tags/form_html.html")
        new_context = Context({"form": form, "btn_text": btn_text, "form_url": form_url},
                              autoescape=context.autoescape)
        print "new_context", new_context
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
        new_context = Context({"request": request}, autoescape=context.autoescape)
        return t.render(new_context)
