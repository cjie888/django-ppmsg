# -*- coding: UTF-8 -*-

from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from ppmsg.forms import ComposeForm 


class ModelTestCases(TestCase):

    def setUp(self):
        TestCase.setUp(self)
        self.client = Client()

    def tearDown(self):
        TestCase.tearDown(self)
        
    def test_save(self):
        pass

    def test_messages_all(self):
        pass

    def test_messages_like(self):
        pass

    def test_messages_between(self):
        pass
class ViewTestCases(TestCase):
    fixtures = ['account.json']
    def setUp(self):
        TestCase.setUp(self)
        self.client = Client()

    def tearDown(self):
        TestCase.tearDown(self)
        
    def test_compose_get(self):
        """ want response_code == 200 and ComposeForm returned """
        compose_url = "/msg/compose/test2/"
        self.client.login(username='test', password='test')
        response = self.client.get(compose_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(isinstance(response.context["form"], ComposeForm))

    def test_compose_get_not_login(self):
        """ want response_code == 302 returned """
        compose_url = "/msg/compose/test2/"
        response = self.client.get(compose_url)
        self.assertTrue(response.status_code == 302)

    def test_compose_post(self):
        """ want response_code == 302 returned """
        compose_url = "/msg/compose/test2/"
        self.client.login(username='test', password='test')
        post_data = {'recipient':'test2', 'content':'test'}
        response = self.client.post(compose_url, post_data)
        self.assertTrue(response.status_code == 302)
        msg_view_url = reverse('ppmsg.views.view')
        self.assertTrue(response['location'].find(msg_view_url))

    def test_compose_post_recipient_not_exists(self):
        """ want response_code == 302 returned """
        compose_url = "/msg/compose/test3/"
        self.client.login(username='test', password='test')
        post_data = {'recipient':'test2', 'content':'test'}
        response = self.client.post(compose_url, post_data)
        self.assertTrue(response.status_code == 302)
        msg_view_url = reverse('ppmsg.views.view')
        self.assertTrue(response['location'].find(msg_view_url))
