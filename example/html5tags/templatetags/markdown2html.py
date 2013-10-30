# -*- coding: utf-8 -*-
import logging

import markdown
from django import template
from django.contrib.markup.templatetags.markup import markdown as django_mark


logger = logging.getLogger(__name__)


register = template.Library()


@register.filter
def markdown2html(content):
    try:
        html_content = markdown.markdown(content,
                                         extensions=['toc', 'tables', 'abbr',
                                                     'codehilite', 'def_list',
                                                     'extra', 'fenced_code',
                                                     'footnotes', 'headerid',
                                                     'meta'])
        return html_content
    except Exception, e:
        logger.error("markdown2html has error: %s." % e)
        return content


@register.filter
def mark(content):
    html_content = django_mark(content, 'safe,toc,tables,abbr,codehilite,def_list,extra,fenced_code,footnotes,headerid,meta')
    return html_content
