#! -*- coding: utf-8 -*-
from django.test import TestCase

from html5tags.templatetags.markdown2html import markdown2html

class MarkdownTestCase(TestCase):
    def test_markdown2html(self):
        content = '* test'
        markdown_content = markdown2html(content)

        self.assertHTMLEqual(markdown_content,"""
        <ul>
            <li>test</li>
        </ul>""")