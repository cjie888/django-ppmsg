django-html5tags is a tag depot which content navbar tag, navigation tag, pagination tag, form tag and so on

Install the app requirements
============================

#. bootstrap - version >= 3
#. markdown - easy_install markdown

Installation
============

#. Add ``"django-html5tags"`` directory to your Python path.
#. Add ``"html5tags"`` to your ``INSTALLED_APPS`` tuple found in
   your settings file. (optional - to be able to run tests)

Testing & Example
=================

There is an example project in the ``example/`` directory. To run
automated tests for django-html5tags run the following command
in ``example/`` directory:

::

    python example/manage.py test html5tags

To run the example project:

::

    python example/manage.py runserver

Then you can visit ``http://localhost:8000/`` to view the example.

Usage
=====

### breadcrumb tag <br/>
example:
<pre>
{% load breadcrumb %}
{% breadcrumb crumbs request %}

crumbs is like: [{"name": "abc", "url": "/"}, {},....]
</pre>

### add_crumb <br/>
the similar function like breadcrumb
example:
<pre>
{% load breadcrumb %}
{% add_crumb 'People' 'people_link' %}

the first parameter represent name which displayed on the page
the second represent url

this result will render to breadcrumb.html
</pre>

### render_navbar <br/>
this tag will render to the page of header
example:
<pre>
{% load navigation %}
{% render_navbar %}

this tag require define something in settings
the followings will illustrate:
LOGIN_URL - login url
LOGOUT_URL - loginout url
REGISTER_URL - register url
SITE_NAME - the name of site

the float height is 70px

</pre>

### render_footer <br/>
example:
<pre>
{% load navigation %}
{% render_footer %}

this tag require define FOOTER in settings
FOOTER like :
	[
		[
			{"name": u"问题反馈", },
			{"name": u"常见问题解答", "url": "/"}
		],
		[
			{"name": u"合作伙伴", },
           	{"name": u"技术支持：应用研发系统组", "url": "/"}
        ]
   ]
the first item of the dict is the title of the footer
</pre>

### horizon_nav <br/>
example:
<pre>
{% load navigation %}
{% horizon_nav "curreant name" all_navs  %}

you can define HORIZON_SECTION in settings
HORIZION_SECTION like:
	[{"name": u"首页", "url": "/"},...]
</pre>

### vertical_nav <br/>
example:
<pre>
{% load navigation %}
{% vertical_nav "current name" all_navs  %}
</pre>

### navtagitem <br/>
the similar function like vertical_nav
example:
<pre>
{% load navigation %}
<ul class="nav nav-pills nav-stacked">
	<li> {% navtagitem "手动添加垂直导航" "/" %}</li>
	<li>{% navtagitem "测试" "/" %}</li>
</ul>
</pre>

### markdown2html <br/>
change the style of markdown into html
example:
<pre>
{% load markdown2html %}
{% markdowncss|markdown2html %}
</pre>

### pagination <br/>
example:
<pre>
{% load pagination %}
{% pagination page_datas prefix request %}
</pre>

### bootstrap <br>
display the form with bootstrap, you must define the submit button by yourself
example:
<pre>
{% load bootstrap %}
{{form|bootstrap}}

the tag dose not support the textarea display with markdown. if you want, you must add js in th html
</pre>

### bootstrap form <br>
rewrite the django form and display the form with bootstrap
example:
<pre>
when you define your form, you can use it lile this:

import html5tags.bootstrap as forms
bootstrap_textarea = forms.MarkDownField()
...

if you use this, you must write the html which is used to display the form by yourself
</pre>
