# -*- coding:utf-8 -*-
from django.template import Context
from django.template.loader import get_template
from django import template
from django import forms

register = template.Library()

@register.tag("render_field")
def render_field(parser, token):
    try:
        tag_name, field, field_container, container_css, label_container, label_css = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments: path and text" % token.split_contents[0]
    return RenderField(field, field_container, container_css, label_container, label_css)

class RenderField(template.Node):
    def __init__(self, field, field_container, container_css, label_container, label_css):
        self.field = template.Variable(field)
        self.field_container = template.Variable(field_container)
        self.container_css = template.Variable(container_css)
        self.label_container = template.Variable(label_container)
        self.label_css = template.Variable(label_css)

    def render(self, context):
        t = template.loader.get_template("render_form_field.html")
        field = self.field.resolve(context)
        field_container = self.field_container.resolve(context)
        container_css = self.container_css.resolve(context)
        label_container = self.label_container.resolve(context)
        label_css = self.label_css.resolve(context)

        new_context = Context({"field": field, "field_container": field_container, "container_css": container_css,
                               "label_container": label_container, "label_css": label_css}, autoescape=context.autoescape)
        return t.render(new_context)