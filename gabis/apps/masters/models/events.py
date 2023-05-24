# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
from datetime import datetime, timedelta
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from django_extensions.db.models import TimeStampedModel

from gabis.apps.users.models import User
from gabis.apps.masters.models.zones import (Keuskupan, Paroki, Wilayah, Lingkungan)

log = logging.getLogger(__name__)


class Event(TimeStampedModel):
    """Event"""
    keuskupan = models.ForeignKey(Keuskupan,
                on_delete=models.CASCADE,
                verbose_name=_("Keuskupan"),
                db_index=True, null=True, blank=True)
    
    paroki = models.ForeignKey(Paroki,
                on_delete=models.CASCADE,
                verbose_name=_("Paroki"),
                db_index=True, null=True, blank=True)
    
    name = models.CharField(
        _("Name"), max_length=100, db_index=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"Event"
        verbose_name_plural = u"002001 Event"
        unique_together = (("keuskupan", "paroki", "name"),)

    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s" % (self.name)
    
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Event, self).save(*args, **kwargs)


class TimeEvent(TimeStampedModel):
    """Time Event"""
    
    event = models.ForeignKey(Event,
                on_delete=models.CASCADE,
                verbose_name=_("Event"),
                db_index=True, null=True, blank=True)
    
    start_time = models.DateTimeField(null=True, blank=True) 
    end_time = models.DateTimeField(null=True, blank=True)
    
    ordered =  models.IntegerField( 
            _("Ordered"),
             help_text = _("Displaying event in ordered."))
    
    max_guest =  models.IntegerField( 
            _("Maximum Guests"),
            default=80,)
    
    booked = models.BooleanField(default=False)
    
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"TimeEvent"
        verbose_name_plural = u"002002 Time Event"
        unique_together = (("event", "start_time", "end_time"),)

    def __init__(self, *args, **kwargs):
        super(TimeEvent, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s %s - %s" % (self.event, self.start_time, self.end_time)
    
    @property
    def group(self):
        return "%s %s" % (_("Kloter"), self.ordered)
    
    @property
    def calendar_start_time_string(self):
        return datetime.strftime(self.start_time, "%Y-%m-%dT%H:%M:%S")
    
    @property
    def calendar_end_time_string(self):
        return datetime.strftime(self.end_time, "%Y-%m-%dT%H:%M:%S")
    
    @property
    def total_guest_book(self):
        from gabis.apps.schedules.models.guestbooks import GuestBook
        gb = GuestBook.objects.filter(time_event=self)
        return len(gb)
    
    @property
    def color(self):
        
        d_now = datetime.now()
        
        if self.total_guest_book >= 80:
            return "gray"
        
        if self.end_time < d_now:
            return "gray"
        
        return "green"
            
        
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user
        
    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(TimeEvent, self).save(*args, **kwargs)
        
        
class PICEvent(TimeStampedModel):
    """Personal Information Contact Event"""
    
    nik = models.CharField(
                _("Nomor Induk Kependudukan Nasional"), 
                max_length=255, db_index=True)
    
    pic = models.CharField(
                _("PIC Event Name"), 
                max_length=255, db_index=True)
    
    event = models.ForeignKey(Event,
                on_delete=models.CASCADE,
                verbose_name=_("Event"),
                db_index=True, null=True, blank=True)
    
    position = models.CharField( 
            _("Position"), 
            max_length=255, null=True, blank=True)
    
    email = models.EmailField( 
        _("Email"),max_length=75, blank=True, null=True)
    
    mobile = models.CharField( 
        _("Mobile"), max_length=64, 
        null=True, blank=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"PICEvent"
        verbose_name_plural = u"002003 PIC Event"
        unique_together = (("nik", "event"),)

    def __init__(self, *args, **kwargs):
        super(PICEvent, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s %s %s" % (self.pic, self.event, self.position)
    

    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(PICEvent, self).save(*args, **kwargs)
        
       
def save_pic_event(sender, instance, created, *args, **kwargs):
    """
        - Create a User
    """
    
    if not isinstance(instance, PICEvent):
       return
    
    if created:
        # Create a group
        pass
    
post_save.connect(save_pic_event, sender=PICEvent)


        