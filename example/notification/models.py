#coding=utf-8
""" notification models
"""

import datetime
import types
from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.db.models.signals import post_save
from django.core import exceptions
# from html5helper import email


DEFAULT_DEVICE_FLAGS = 0x0001


def create_notice_type(label, display, description, **kwargs):
    return NoticeType.create(label, display, description, **kwargs)
    

class NoticeType(models.Model):
    
    label = models.CharField(max_length=40)
    display = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    # by default only on for media with sensitivity less than or equal to this number
    flags = models.IntegerField(default=DEFAULT_DEVICE_FLAGS)
    
    def __unicode__(self):
        return self.label
    
    class Meta:
        app_label = "notification"
        ordering = ["label"]
    
    @classmethod
    def create(cls, label, display, description, flags=DEFAULT_DEVICE_FLAGS, verbosity=1):
        """
        Creates a new NoticeType.
        
        This is intended to be used by other apps as a post_syncdb manangement step.
        """
        try:
            notice_type = cls._default_manager.get(label=label)
            updated = False
            if display != notice_type.display:
                notice_type.display = display
                updated = True
            if description != notice_type.description:
                notice_type.description = description
                updated = True
            if flags != notice_type.flags:
                notice_type.flags = flags
                updated = True
            if updated:
                notice_type.save()
                if verbosity > 1:
                    print "Updated %s NoticeType" % label
        except cls.DoesNotExist:
            notice_type = cls(label=label, display=display, description=description, flags=flags)
            notice_type.save()
            if verbosity > 1:
                print "Created %s NoticeType" % label
                
        return notice_type
    

class NoticeSettingManager(models.Manager):
    def myself(self, user):
        result = []
        notice_types = NoticeType.objects.all()
        for notice_type in notice_types:
            try:
                notice_setting = super(NoticeSettingManager, self).get_query_set().get(user=user, notice_type=notice_type)
            except exceptions.ObjectDoesNotExist:
                notice_setting = NoticeSetting(user=user, notice_type=notice_type, flags=notice_type.flags)
                notice_setting.save()
            result.append(notice_setting)
        
        return result


class NoticeSetting(models.Model):
    DEVICE_WEB = 0
    DEVICE_EMAIL= 1
    DEVICE_CHOICES = (
        (DEVICE_WEB, u"网站"),
        (DEVICE_EMAIL, u"邮箱"),
    )
    
    user = models.ForeignKey(DjangoUser)
    notice_type = models.ForeignKey("NoticeType")
    flags = models.IntegerField(default=DEFAULT_DEVICE_FLAGS)
    add_datetime = models.DateTimeField(default = lambda: datetime.datetime.now())
    objects = NoticeSettingManager()
    
    class Meta:
        app_label = "notification"  
        
    def devices_tuple(self):
        """ used for form
        """
        result = []
        for (device, name) in self.DEVICE_CHOICES:
            if device_is_set(self.flags, device):
                result.append(device)    
        return tuple(result)
    
    
class NoticeManager(models.Manager):
    def unread(self, user, device):
        notices = super(NoticeManager, self).get_query_set().filter(is_read=False, user=user)
        result = []
        for notice in notices:
            if notice.is_could_send(device):
                result.append(notice)
                
        return result
    
    def unread_of_email(self, user):
        return self.unread(user, NoticeSetting.DEVICE_EMAIL)
    
    def unread_of_web(self, user):
        return self.unread(user, NoticeSetting.DEVICE_WEB)
    
    def unread_and_unsend(self, user, device):
        unreads = self.unread(user, device)
        result = []
        for notice in unreads:
            if notice.is_could_send(device) is False:
                continue
            result.append(notice)
            
        return result
    
    def unread_and_unsend_of_web(self, user):
        return self.unread_and_unsend(user, NoticeSetting.DEVICE_WEB)
    
    def unread_and_unsend_of_email(self, user):
        return self.unread_and_unsend(user, NoticeSetting.DEVICE_EMAIL)
                
        
        
class Notice(models.Model):
    user = models.ForeignKey(DjangoUser)
    notice_type = models.ForeignKey("NoticeType")
    target = models.URLField(max_length = 1024, null = True, blank = True)
    content = models.CharField(max_length = 1024)
    is_read = models.BooleanField(default = False)
    sent_device = models.IntegerField(default = 0) # bit flag
    add_datetime = models.DateTimeField(default=lambda:datetime.datetime.now())
    reminder_value = models.IntegerField(null = True)
    last_reminder_time = models.DateTimeField(null = True)
    objects = NoticeManager()
    
    class Meta:
        app_label = "notification"
        ordering = ["-add_datetime"]
        
    def is_could_send(self, device):
        try:
            notice_setting = NoticeSetting.objects.get(user=self.user, notice_type=self.notice_type)
        except exceptions.ObjectDoesNotExist:
            notice_setting = None
        
        if notice_setting:
            return device_is_set(notice_setting.flags, device)
        
        return device_is_set(self.notice_type.flags, device)
                    
    @classmethod
    def push(cls, user, notice_type, target, content, **kwargs):
        """ if target has exists, do't allow to add
        params:
           user: user object
           target: target url link
           notice_type: notice type
           content: content
        """
        try:
            notice = cls.objects.get(user=user, notice_type=notice_type, target=target)
        except exceptions.ObjectDoesNotExist:
            notice = cls.objects.create(user=user, notice_type=notice_type, target=target, content=content, **kwargs)
        
        return notice
    
    @classmethod
    def replace(cls, user, notice_type, target, content, **kwargs):
        """ if target has exists, replace its content and add datetime, and set is_read as False
        Params:
           user: user object
           target: target url link
           notice_type: notice type
           content: content
        Returns:
           Notification object
        """
        try:
            notification = cls.objects.get(user=user, target=target, notice_type=notice_type)
            notification.content = content 
            notification.add_datetime = datetime.datetime.now()
            notification.is_read = False
            notification.save()
        except exceptions.ObjectDoesNotExist:
            notification = cls.objects.create(user=user, notice_type=notice_type, target=target, content=content, **kwargs)
        
        return notification
        
    
    @classmethod
    def send_to_email(cls, user):
        """ send all unread notification to owner, don't run in foreground
        """
        #send to email now
        unsends = cls.objects.unread_and_unsend_of_email(user)
        if len(unsends) == 0:
            return
        
        subject = u"您有%d条通知待处理" % len(unsends)
#         email.send_html_mail(subject, "notification/notice_email.html", {"notifications": unsends}, user.email)
        
        for notice in unsends:
            notice.sent_device = devices_set_true(notice.sent_device, 
                                                    [NoticeSetting.DEVICE_EMAIL])
            notice.save()
            
            
def device_is_set(flags, device):
    """ notice: device don't bigger than 32. flags is int
    """
    and_result = flags & (0x0001 << device)
    right_move_result = and_result >> device
    return bool(right_move_result)


def devices_set_true(flags, devices):
    """ return new flags 
    """
    result = flags
    for device in devices:
        if not isinstance(device, types.IntType):
            device = int(device)
        result = (0x0001 << device) | result
    return result