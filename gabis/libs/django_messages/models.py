from __future__ import unicode_literals, absolute_import

import logging

from datetime import datetime

from django.conf import settings
from django.urls import reverse, reverse_lazy

from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Mongo
from mongoengine import connect, disconnect
from mongoengine import signals as mongo_signals
from bson import ObjectId

from django_mongoengine import Document, EmbeddedDocument, fields


log = logging.getLogger(__name__)

# connect(settings.MONGODB_DATABASES['django_messages']['name'], alias='django_messages')
connect(db=settings.MONGODB_DATABASES['django_messages']['name'],
        host=settings.MONGODB_DATABASES['django_messages']['host'],
        username=settings.MONGODB_DATABASES['django_messages']['username'],
        password=settings.MONGODB_DATABASES['django_messages']['password'], alias='django_messages')


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            recipient=user.username,
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user.username,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user.username,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )


class Message(Document):
    """
    A private message from user to user
    """
   
    subject = fields.StringField(max_length=255)
    body = fields.StringField()
    
    sender = fields.StringField(max_length=255) #user_name
    recipient = fields.StringField(max_length=255) #useer_name
    
    parent_msg = fields.ReferenceField("self", null=True, blank=True)
    
    sent_at = fields.DateTimeField(
        null=True, blank=True
    )
    read_at = fields.DateTimeField(
        null=True, blank=True
    )
    replied_at = fields.DateTimeField(
        null=True, blank=True
    )
    sender_deleted_at = fields.DateTimeField(
        null=True, blank=True
    )
    recipient_deleted_at = fields.DateTimeField(
        null=True, blank=True
    )
    

    created = fields.DateTimeField(
        default=datetime.now(), editable=False,
    )
    
    updated = fields.DateTimeField(
        default=datetime.now(), editable=True,
    )
    
    user_update = fields.StringField(
            max_length=30, blank=True, null=True)
    
    meta = dict(
        db_alias='django_messages'
        )
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        
        
    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self._user_update = None
        
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

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('messages:messages_detail', args=[self.id])
    
    
    @classmethod
    def post_save(cls, sender, document, **kwargs):
        from gabis.libs.django_messages.utils import new_message_email
        new_message_email
        
        
        
    def save(self, *args, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
            
        self.user_update = self._user_update
        
        super(Message, self).save(*args, **kwargs)
        
        
    

def inbox_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()

# fallback for email notification if django-notification could not be found
if "pinax.notifications" not in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    mongo_signals.post_save.connect(Message.post_save, sender=Message)
    
    
    
    
# class Message(models.Model):
#     """
#     A private message from user to user
#     """
#     subject = models.CharField(_("Subject"), max_length=140)
#     body = models.TextField(_("Body"))
#     sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', verbose_name=_("Sender"), on_delete=models.PROTECT)
#     recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages', null=True, blank=True, verbose_name=_("Recipient"), on_delete=models.SET_NULL)
#     parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name=_("Parent message"), on_delete=models.SET_NULL)
#     sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
#     read_at = models.DateTimeField(_("read at"), null=True, blank=True)
#     replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
#     sender_deleted_at = models.DateTimeField(_("Sender deleted at"), null=True, blank=True)
#     recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), null=True, blank=True)
# 
#     objects = MessageManager()
# 
#     def new(self):
#         """returns whether the recipient has read the message or not"""
#         if self.read_at is not None:
#             return False
#         return True
# 
#     def replied(self):
#         """returns whether the recipient has written a reply to this message"""
#         if self.replied_at is not None:
#             return True
#         return False
# 
#     def __str__(self):
#         return self.subject
# 
#     def get_absolute_url(self):
#         return reverse('messages:messages_detail', args=[self.id])
# 
#     def save(self, **kwargs):
#         if not self.id:
#             self.sent_at = timezone.now()
#         super(Message, self).save(**kwargs)
# 
#     class Meta:
#         ordering = ['-sent_at']
#         verbose_name = _("Message")
#         verbose_name_plural = _("Messages")
        
# if "pinax.notifications" not in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
#     from gabis.libs.django_messages.utils import new_message_email
#     signals.post_save.connect(new_message_email, sender=Message)
        
        
        
        
        
        
        
        
