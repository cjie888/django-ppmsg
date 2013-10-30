# -*- coding:utf-8 -*-
from django.template import Context
from django.template.loader import get_template
from django import template
from django import forms

register = template.Library()

@register.filter
def bootstrap(element):
    markup_classes = {'label': '', 'value': ''}
    return render(element, markup_classes)


@register.filter
def bootstrap_inline(element):
    markup_classes = {'label': 'sr-only', 'value': ''}
    return render(element, markup_classes)


def add_input_classes(field):
    if not is_checkbox(field) and not is_multiple_checkbox(field) and not is_radio(field) and not is_file(field):
        field_classes = field.field.widget.attrs.get('class', '')
        field_classes += ' form-control'
        field.field.widget.attrs['class'] = field_classes


def render(element, markup_classes):
    element_type = element.__class__.__name__.lower()

    if element_type == 'boundfield':
        add_input_classes(element)
        template = get_template("bootstrapform/field.html")
        context = Context({'field': element, 'classes': markup_classes})
    else:
        has_management = getattr(element, 'management_form', None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template = get_template("bootstrapform/formset.html")
            context = Context({'formset': element, 'classes': markup_classes})
        else:
            for field in element.visible_fields():
                add_input_classes(field)
            template = get_template("bootstrapform/form.html")
            context = Context({'form': element, 'classes': markup_classes})

    return template.render(context)


@register.filter
def is_radioselect(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_date(field):
    return isinstance(field.field.widget, forms.DateInput)


@register.filter
def is_datetime(field):
    return isinstance(field.field.widget, forms.DateTimeInput)


@register.filter
def is_time(field):
    return isinstance(field.field.widget, forms.TimeInput)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, (forms.ClearableFileInput, ))
