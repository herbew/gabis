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
from gabis.apps.schedules.models.bookings import BookingTimeEvent

log = logging.getLogger(__name__)

class GuestBook(TimeStampedModel):
    """GuestBook"""
    
    GENDER_CHOICES = (
        ('m',_('Male')),
        ('f',_('Female')),
    )
    
    time_event = models.ForeignKey(TimeEvent,
                on_delete=models.CASCADE,
                verbose_name=_("Time Event"),
                db_index=True, null=True, blank=True)
    
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
    
    nik = models.CharField(
                _("No Identitas"), 
                help_text='KTP/Nomor HP',
                max_length=255, db_index=True)
    
    name = models.CharField(
                _("Name"), 
                max_length=255, db_index=True)
    
    gender = models.CharField( 
            _("Gender"), 
            choices=GENDER_CHOICES, 
            max_length=1, 
            null=True, blank=True)
    
    age =  models.IntegerField( 
            _("Age"))
    
    email = models.EmailField( 
        _("Email"),max_length=75, blank=True, null=True)
    
    mobile = models.CharField( 
        _("Mobile"), max_length=64, 
        null=True, blank=True)
    
    pin = models.CharField( 
        _("PIN of Guest"), max_length=64, 
        null=True, blank=True)
    
    attended = models.BooleanField(default=False) #This for payment verification
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'schedules'
        verbose_name = u"GuestBook"
        verbose_name_plural = u"002001 Guest Book"
        
        unique_together = (("time_event", "nik"),)

    def __init__(self, *args, **kwargs):
        super(GuestBook, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s %s:%s-%s" % (self.time_event, self.wilayah, self.lingkungan, self.nik)
    
        
    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(GuestBook, self).save(*args, **kwargs)

def save_guest_book(sender, instance, created, *args, **kwargs):
    """
        - Create a User
    """
    
    if not isinstance(instance, GuestBook):
       return
    
    if created:
        # # Create a group
        # r = get_random()
        # while GuestBook.objects.filter(pin=r):
        #     r = get_random()
        #
        # instance.pin = r
        # instance.save()
        pass
    
post_save.connect(save_guest_book, sender=GuestBook)



