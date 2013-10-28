# -*- coding: utf-8 -*-

import datetime, sys, time
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django import forms
from toollib.render import render_template, render_json
from ppmsg.models import Message, message_count_unread
from ppmsg.forms import ComposeForm

@login_required
def compose(request, recipient=None, form_class=ComposeForm,
        template_name='compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """
    if request.method == "POST":
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, u"Message successfully sent.")
            if success_url is None:
                success_url = reverse('messages_view')
            if request.GET.has_key('next'):
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
        if recipient is not None:
            recipients = [u for u in User.objects.filter(**{'%s__in' % 'username': [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipients
    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'私信','url':'/msg/view/'},{'name': u'写私信 '}]
    return render_template(template_name, request, form = form, breadcrumb=breadcrumb)

@login_required
@render_json
def delete(request, message_id):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely. 
    A cron-job should prune the database and remove old messages which are 
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.
    
    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`).
    """
    user = request.user
    now = datetime.datetime.now()
    message = get_object_or_404(Message, id=message_id)
    deleted = False
    if message.sender == user:
        message.sender_deleted_at = now
        deleted = True
    if message.recipient == user:
        message.recipient_deleted_at = now
        deleted = True
    if deleted:
        message.save()
        messages.info(request, u"Message successfully deleted.")
        #if notification:
        #   notification.send([user], "messages_deleted", {'message': message,})
        return {'status': 'ok', 'msg': u'删除成功!'}
    return {'status': 'nok', 'msg': u'删除失败!'}

@login_required
@render_json
def delete_session(request, username, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely. 
    A cron-job should prune the database and remove old messages which are 
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.
    
    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    session_user = User.objects.get(username=username)
    try:
        Message.objects.filter(sender=request.user, recipient=session_user, sender_deleted_at__isnull=True).update(sender_deleted_at=datetime.datetime.now())
        Message.objects.filter(sender=session_user, recipient=request.user, recipient_deleted_at__isnull=True).update(recipient_deleted_at=datetime.datetime.now())
        return {'status': 'ok', 'msg': u'删除成功!'}
    except Exception, e:
        return {'status': 'nok', 'msg': u'删除失败!'}
    
@login_required
@render_json
def set_read(request, username, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it's save to remove it completely. 
    A cron-job should prune the database and remove old messages which are 
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.
    
    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    session_user = User.objects.get(username=username)
    try:
        Message.objects.filter(sender=session_user, recipient=request.user, read_at__isnull=True).update(read_at=datetime.datetime.now())
        return {'status': 'ok', 'msg': u'设置成功!'}
    except Exception, e:
        return {'status': 'nok', 'msg': u'设置失败!'}

@login_required
def view(request, template_name='view.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either 
    the sender or the recipient. If the user is not allowed a 404
    is raised. 
    If the user is the recipient and the message is unread 
    ``read_at`` is set to the current datetime.
    """
    cond = None
    if 'cond' in request.GET:
        cond = request.GET['cond']
    if cond:
        message_list = Message.objects.messages_like(request.user, cond)
    else:
        message_list = Message.objects.messages_all(request.user)
    user_lastmsgs = {}
    for message in message_list:
        if message.sender not in user_lastmsgs and message.sender != request.user:
            user_lastmsgs[message.sender] = message
        if message.recipient not in user_lastmsgs and message.recipient != request.user:
            user_lastmsgs[message.recipient] = message
    msg_unreads = {}
    for user in user_lastmsgs:
        msg_unreads[user] = message_count_unread(user, request.user)
    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'私信'}]
    return render_template(template_name, request, users = user_lastmsgs, unreads = msg_unreads, breadcrumb=breadcrumb)

@login_required
def view_detail(request, username, template_name='view_detail.html'):
    """
    Shows a single message.``message_id`` argument is required.
    The user is only allowed to see the message, if he is either 
    the sender or the recipient. If the user is not allowed a 404
    is raised. 
    If the user is the recipient and the message is unread 
    ``read_at`` is set to the current datetime.
    """
    session_user = User.objects.get(username=username)
    message_list = Message.objects.messages_between(request.user, session_user)
    breadcrumb = [{"name": u"首页", "url": "/"}, {'name': u'私信','url':'/msg/view/'},{'name': u'与 ' + session_user.username + u'的会话'}]
    #Message.objects.filter(recipient=request.user, sender=recipients[0], read_at__isnull=True).update(read_at=datetime.datetime.now())
    return render_template(template_name, request, message_list = message_list, session_user= session_user, breadcrumb=breadcrumb)