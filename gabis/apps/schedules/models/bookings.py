# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from django_extensions.db.models import TimeStampedModel

from gabis.apps.users.models import User

from gabis.apps.masters.models.zones import (Keuskupan, Paroki, Wilayah, Lingkungan)
from gabis.apps.masters.models.events import TimeEvent

log = logging.getLogger(__name__)


class BookingTimeEvent(TimeStampedModel):
    """BookingTimeEvent"""
    
    time_event = models.ForeignKey(TimeEvent,
                on_delete=models.CASCADE,
                verbose_name=_("Time Event"),
                db_index=True)
    
    keuskupan = models.ForeignKey(Keuskupan,
                on_delete=models.CASCADE,
                verbose_name=_("Keuskupan"),
                db_index=True, null=True, blank=True)
    
    paroki = models.ForeignKey(Paroki,
                on_delete=models.CASCADE,
                verbose_name=_("Paroki"),
                db_index=True, null=True, blank=True)
    
    wilayah = models.ForeignKey(Wilayah,
                on_delete=models.CASCADE,
                verbose_name=_("Wilayah"),
                db_index=True, null=True, blank=True)
    
    lingkungan = models.ForeignKey(Lingkungan,
                on_delete=models.CASCADE,
                verbose_name=_("Lingkungan"),
                db_index=True, null=True, blank=True)
    
    group = models.CharField(
                _("Name Group"), 
                max_length=100, db_index=True)
    
    pic_group = models.CharField(
                _("PIC Group"), 
                max_length=255, db_index=True)
    
    email = models.EmailField( 
        _("Email"),max_length=75, blank=True, null=True)
    
    mobile = models.CharField( 
        _("Mobile"), max_length=64, 
        null=True, blank=True)
    
    url_guest_book = models.TextField(  
                _("Link Guest Book"), 
                null=True, blank=True
                )
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'schedules'
        verbose_name = u"BookingTimeEvent"
        verbose_name_plural = u"001001 Booking Time Event"
        
        unique_together = (("time_event", "keuskupan", "paroki", "wilayah", "lingkungan", "group"),)

    def __init__(self, *args, **kwargs):
        super(BookingTimeEvent, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s %s:%s-%s" % (self.time_event, self.wilayah, self.lingkungan, self.group)
    
        
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(BookingRoom, self).save(*args, **kwargs)

def save_booking_time_event(sender, instance, created, *args, **kwargs):
    """
        - Create a User
    """
    
    if not isinstance(instance, BookingTimeEvent):
       return
    
    if created:
        # Create a group
        pass
    
post_save.connect(save_booking_time_event, sender=BookingTimeEvent)


def delete_booking_time_event(sender, instance,  *args, **kwargs):
    """delete booking_time_event"""
    
    if not isinstance(instance, BookingTimeEvent):
       return
    
    te = TimeEvent.objects.get(id=instance.time_event.id)
    te.booked = False
    te.save()
    
pre_delete.connect(delete_booking_time_event, sender=BookingTimeEvent)
