#coding=utf-8

import datetime
import time
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import render
from toollib.page import get_page
from toollib.render import render_template, render_json
from notification.models import Notice, NoticeSetting, devices_set_true, NoticeList
from notification import config
from notification.forms import NoticeSettingForm
from notification.tables import NoticeTable

# from html5helper.utils import do_paginator
# from html5helper.decorator import render_template, render_json




@login_required
def home(request, page_no=1):
    notices = Notice.objects.filter(user=request.user) 
    prefix = reverse("notification.views.home")
    current_nav = u"通知中心"
    breadcrumbs = [
        {"name": current_nav},
    ]
    for notice in notices:
        add_datetime_timestamp = time.mktime(notice.add_datetime.timetuple())
        add_datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(add_datetime_timestamp))
        if notice.is_read == 1:
            NoticeList.push(add_datetime=add_datetime, content=notice.content) 
        else:
            content="<a href=\"%s\" target=\"_blank\" >%s</a>" % (notice.target, notice.content)
            NoticeList.push(add_datetime=add_datetime, content=content)
    show_notices = NoticeTable()
    return render_template("notification/home.html", request=request, prefix=prefix, \
                           show_notices=show_notices, breadcrumbs=breadcrumbs,
                           current_nav=current_nav)


@login_required
def change(request):
    notice_settings = NoticeSetting.objects.myself(request.user)
    
    if request.method == "POST":
        form = NoticeSettingForm(request.POST, user=request.user)
        if form.is_valid():
            for notice_setting in notice_settings:
                notice_setting.flags = devices_set_true(notice_setting.flags, form.cleaned_data[notice_setting.notice_type.label])
                notice_setting.save()
            messages.success(request, u"成功修改通知")
            
            return redirect(reverse("notification.views.change"))
    else:
        data = {}
        for notice_setting in notice_settings:
            data[notice_setting.notice_type.label] = notice_setting.devices_tuple()
        form = NoticeSettingForm(data, user=request.user)
    
    current_nav = u"设置"
    breadcrumbs = [
        {"name":u"通知中心", "url":reverse("notification.views.home")},
        {"name":current_nav},
    ]
    return render_template("notification/change.html", form=form, request=request, breadcrumbs=breadcrumbs, 
                           current_nav=current_nav)


@login_required
def go(request, notice_id):
    try:
        notice = Notice.objects.get(id = notice_id)
    except:
        messages.warning(request, u"该通知已经过期")
        return redirect(reverse("notification.views.home"))
    
    notice.is_read = True
    notice.save()
    return redirect(notice.target)


@login_required
@render_json
def my(request):
    is_ok = False
    # check notifications
    notices = Notice.objects.unread_of_web(request.user)
    if len(notices) > 0:
        is_ok = True
        init_reasons = []
        reasons = get_reasons(init_reasons, notices)
    return {"is_ok": is_ok, "reason": ".".join(reasons), "reasons": reasons}

def get_reasons(reasons, notices):
    for notice in notices:
        print notice
        reminder_flag = get_reminder_flag(notice)
        print reminder_flag 
        if reminder_flag != 0:
            if reminder_flag == 1:
                update_notice(notice)
            reasons.append(mark_safe("<span class='text-muted'>%s</span> <a href='%s' target='_blank'>%s</a>" % (
                                    notice.add_datetime,
                                    reverse("notification.views.go", args=[notice.id]), 
                                    notice.content)))
            print reasons
    return reasons
    
def get_reminder_flag(notice, unit_timestamp=config.ONE_DAY_SECONDS):
    reminder_flag = 0
    if notice.last_reminder_time is None:
        initialize_notice(notice)
        reminder_flag = 2
    else:
        now_timestamp = time.time()
        last_reminder_timestamp = time.mktime(notice.last_reminder_time.timetuple())
        between_days = int(now_timestamp - last_reminder_timestamp) / unit_timestamp
        print between_days
        if between_days >= notice.reminder_value:
            reminder_flag = 1    
    return reminder_flag

def initialize_notice(notice):
    if notice.last_reminder_time is None:
        notice.last_reminder_time = datetime.datetime.now()
        notice.save()
    if notice.reminder_value is None:
        notice.reminder_value = 1
        notice.save()

def update_notice(notice):
    if notice.reminder_value >= config.MAX_REMINDER_VALUE:
        notice.is_read = 1
        notice.save()
    else:
        #艾宾浩斯遗忘曲线公式
        notice.reminder_value = notice.reminder_value + notice.reminder_value * notice.reminder_value
        notice.save()
    notice.last_reminder_time = datetime.datetime.now()
    notice.save()
    


@login_required
@render_json
def clear(request):
    # check notifications
    notices = Notice.objects.unread_of_web(request.user)
    for notice in notices:
        notice.is_read = True
        notice.save()
        
    return {"is_ok":True}
