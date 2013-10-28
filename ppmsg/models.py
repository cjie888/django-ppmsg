# -*- coding: UTF-8 -*-
import datetime
from django.db import models
from django.conf import settings
from django.db.models import signals

from django.contrib.auth.models import User


class MessageManager(models.Manager):

    def messages_all(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are not marked as deleted.
        """
        return (self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )).order_by('-sent_at')
    def messages_like(self, user, cond):
        """
        Returns all messages that were either received or sent by the given
        user and are not marked as deleted.
        """
        return (self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
            content__icontains=cond,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
            content__icontains=cond,
        )).order_by('-sent_at')
    def messages_between(self, user_from, user_to):
        """
        Returns all messages that were between two user and are not marked as deleted.
        """
        return (self.filter(
            recipient=user_from,
            recipient_deleted_at__isnull=True,
        ) & self.filter(
            sender=user_to,
            sender_deleted_at__isnull=True,
        )| self.filter(
            recipient=user_to,
            recipient_deleted_at__isnull=True,
        ) & self.filter(
            sender=user_from,
            sender_deleted_at__isnull=True,
        )).order_by('-sent_at')

class Message(models.Model):
    """
    A private message from user to user
    """
    content = models.CharField("content", max_length=120)
    sender = models.ForeignKey(User, related_name='sent_messages', verbose_name="Sender")
    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True)
    sent_at = models.DateTimeField("sent at", null=True, blank=True)
    read_at = models.DateTimeField("read at", null=True, blank=True)
    sender_deleted_at = models.DateTimeField("Sender deleted at", null=True, blank=True)
    recipient_deleted_at = models.DateTimeField("Recipient deleted at", null=True, blank=True)
    
    objects = MessageManager()
    
    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True
        
    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False
    
    def __unicode__(self):
        return self.content
    
    def get_absolute_url(self):
        return ('messages_detail', [self.id])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def save(self, **kwargs):
        if not self.id:
            self.sent_at = datetime.datetime.now()
        super(Message, self).save(**kwargs) 
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"

def message_count_unread(user_from, user_to):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Message.objects.filter(sender=user_from, recipient=user_to, read_at__isnull=True, recipient_deleted_at__isnull=True).count()
