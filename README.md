A user-to-user messaging system for Django
==========================================
Django-ppmsg enables your users to send private messages to each other. 
It provides a basic set of functionality that you would expect from such a system.

If you have any question, please contact **dev-web-sys@funshion.com** 

Github link: <https://github.com/cjie888/django-ppmsg>
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

###  Add  above app to your ``INSTALLED_APPS`` setting.
    <pre> 
    INSTALLED_APPS += (
        'toollib',
        'html5tags',
        'avatar',
        'acount',
        'notification',
        'ppmsg',
        )
    </pre>

###  Add url conf to your urls.py.
<br/>
<pre>
url(r'msg/', include('ppmsg.urls')),
</pre>

### The page which you can use:
/msg/view/  Display the private message of the current login user <br/>
/msg/compose/ Compose private message


Advanced Usage
-----
### Use tag.
<br/>
compose message tag:
<pre>
{% load message_tags %}
{% compose_msg '/msg/view/'%}
Note: The parameter is the redirect page when the login user successfully send the message.
</pre>
view message tag:
<pre>
{% load message_tags %}
{% messages request %}
Note：the request parameter is the HTTPRequest object.
</pre>

Sites that use django-ppmsg
-----
Not yet now.