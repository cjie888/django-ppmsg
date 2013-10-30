#! -*- coding: utf-8 -*-
from django.utils import unittest
from django.http import HttpRequest 

from html5tags.templatetags.breadcrumb import render_breadcrumbs

class CrumbsTestCase(unittest.TestCase):
    def test_render_without_request(self):
        response = render_breadcrumbs({})

        self.assertEqual(response, {"breadcrumb": None})

    def test_render_with_request(self):
        response = render_breadcrumbs({'request': ''})

        self.assertEqual(response, {"breadcrumb": None})

    def test_render_with_request_and_crumbs(self):
        context = {}
        context['request'] = HttpRequest()
        context['request'].breadcrumbs = []
        context['request'].breadcrumbs.append(('Test1', '/'))
        context['request'].breadcrumbs.append(('Test2', '/'))
        response = render_breadcrumbs(context)
        self.assertEqual(response, {'breadcrumb': [('Test1', '/'), ('Test2', '/')]})

    def test_add_without_request(self):
        response = render_breadcrumbs({})

        self.assertEqual(response, {"breadcrumb": None})

    def test_add_with_request(self):
        response = render_breadcrumbs({'request': ''})

        self.assertEqual(response, {"breadcrumb": None})
