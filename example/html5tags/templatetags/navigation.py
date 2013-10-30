# -*- coding: utf-8 -*-
import copy

from django import template
from django.template import Context


register = template.Library()


@register.tag("render_navbar")
def narbar(parser, token):
    try:
        tag_name, buttons = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments: path and text" % token.split_contents[0]
    return NavBar(buttons)

class NavBar(template.Node):
    def __init__(self, buttons):
        self.buttons = template.Variable(buttons)

    def render(self, context):
        t = template.loader.get_template("nav_bar.html")
        request = context["request"]
        settings = context["settings"]
        buttons = self.buttons.resolve(context)

        new_context = Context({"request": request, "settings": settings, "buttons": buttons},
                              autoescape=context.autoescape)
        return t.render(new_context)


@register.tag("navtagitem")
def navtagitem(parser, token):
    try:
        tag_name, nav_text, nav_path = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments: path and text" % token.split_contents[0]

    return NavTagItem(nav_text, nav_path)

class NavTagItem(template.Node): 
    def __init__(self, nav_displaytext, nav_path):
        self.path = nav_path.strip('"')
        self.text = nav_displaytext.strip('"')

    def render(self, context):
        return '<a href="%s">%s</a>' % (self.path, self.text)


@register.tag("horizon_nav")
def do_horizontal_nav(parser, token):
    try:
        tag_name, tab, tabs = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return HorizontalNavNode(tab, tabs)

class HorizontalNavNode(template.Node):
    def __init__(self, tab, tabs):
        self.tab = template.Variable(tab)
        self.tabs = template.Variable(tabs)

    def render(self, context):
        t = template.loader.get_template("horizontal_nav.html")
        tabs = copy.deepcopy(self.tabs.resolve(context))
        cur_tab = self.tab.resolve(context)
        for tab in tabs:
            if tab["name"] == cur_tab:
                tab["is_active"] = 1
        new_context = Context({'tabs': tabs}, autoescape=context.autoescape)
        return t.render(new_context)


@register.tag("vertical_nav")
def do_vertical_nav(parser, token):
    try:
        tag_name, tab, tabs = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return VerticalNavNode(tab, tabs)

class VerticalNavNode(template.Node):
    def __init__(self, tab, tabs):
        self.tab = template.Variable(tab)
        self.tabs = template.Variable(tabs)

    def render(self, context):
        t = template.loader.get_template("vertical_nav.html")
        tabs = self.tabs.resolve(context)
        cur_tab = self.tab.resolve(context)
        new_context = Context({'cur_tab': cur_tab, 'tabs': tabs}, autoescape=context.autoescape)
        return t.render(new_context)


@register.inclusion_tag("footer.html", takes_context=True)
def render_footer(context):
    if "settings" in context and hasattr(context["settings"], "FOOTER"):
        footers = context["settings"].FOOTER
    else:
        footers = None
    if footers and len(footers) == 0:
        footers = None
    return {"footers": footers}
