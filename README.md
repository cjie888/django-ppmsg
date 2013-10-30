==========================================
A user-to-user messaging system for Django
==========================================
Django-ppmsg enables your users to send private messages to each other. 
It provides a basic set of functionality that you would expect from such a system.

Install
-------
You should to copy the following apps into your project:

- **toollib**
   toollib is a common module for rendering template, pagination, verfication code etc 
- **html5tags**
   html5tags provide basic style for comment form and pagination   
- **acount**
   application acount is responsible for login and logout
- **notification**
   the message notification system
- **ppmsg**
   the private message
   
Usage
-----

1. Add  above app to your ``INSTALLED_APPS`` setting.
    <pre> INSTALLED_APPS += (
        'toollib',
        'html5tags',
        'avatar',
        'acount',
        'notification',
        'ppmsg',
        )</pre>
2. Add url conf to your urls.py.
<pre>
from ppmsg.views import *
url(r'^msg/compose/$', compose, name='messages_compose'),
url(r'^msg/compose/(?P<recipient>[\w.@+-]+)/$', compose, name='messages_compose_to'),
url(r'^msg/search/$', view, name='messages_search'),
url(r'^msg/view/$', view, name='messages_view'),
url(r'^msg/detail/(?P<username>[\w.@+-]+)/$', view_detail, name='messages_detail'),
url(r'^msg/delete_session/(?P<username>[\w.@+-]+)/$', delete_session, name='messages_delete_session'),
url(r'^msg/set_read/(?P<username>[\w.@+-]+)/$', set_read, name='messages_set_read'),
url(r'^msg/delete/(?P<message_id>[\d]+)/$', delete, name='messages_delete'),
</pre>
3. use tag <br/>
compose message tag:
<pre>
{% load message_tags %}
{% compose_msg '/msg/view/' %}
</pre>
view message tag:
<pre>
{% load message_tags %}
{% messages request %}
</pre>