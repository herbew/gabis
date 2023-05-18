# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import pytz
import logging
from datetime import datetime, timedelta, date

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from gabis.core.choices import USER_CHOICES

log = logging.getLogger(__name__)


class User(AbstractUser):
    
    USER_CHOICES = USER_CHOICES
    
    GENDER_CHOICES = (
        ('m',_('Male')),
        ('f',_('Female')),
    )
    
    name = models.CharField(
            _("Complete Name"), 
            max_length=250)
    
    
    types = models.CharField( _("Type"), 
            choices=USER_CHOICES, 
            max_length=3,
            null=True, blank=True)
    
    birth_city = models.CharField(
            _("Birth City"), 
            max_length=100, 
            null=True, blank=True)
    
    birth_date = models.DateField(
            _("Birth Date"), 
            null=True, blank=True)
    
    gender = models.CharField( 
            _("Gender"), 
            choices=GENDER_CHOICES, 
            max_length=1, 
            null=True, blank=True)
    
    address = models.TextField(
            _("Address"), 
            null=True, blank=True)
    
    mobile = models.CharField( 
            _("Mobile"), 
            max_length=64, 
            null=True, blank=True)
    
    created = models.DateTimeField(
            _("Create"), 
            null=True, blank=True)
    
    modified = models.DateTimeField(
            _("Modified"), 
            null=True, blank=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)
    
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self._user_update = None
         
    def __str__(self):
        
        if self.name:
            return self.name
        
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
    
    @property
    def get_latest_timezone(self):
        """TimeZone was sign if user have a created a schedule or booking room"""
        
        from gabis.apps.schedules.models.users import UserBookingRoom
        
        ubr = UserBookingRoom.objects.filter(users=self).order_by("-created")
        
        if ubr:
            return ubr[0]
        return None
    
    @property
    def get_address(self):
        return [a for a in self.address.split('\n') if not a in[None,""]]
    
    @property
    def get_email(self):
        
        if self.email:
            if len(self.email) > 26:
                return "%s --" % (self.email[:20])
            
        return self.email

    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")
    
    def save(self, *args, **kwargs):
        
        if not self.pk:
            #created
            self.created = datetime.now()
            
        self.modified = datetime.now()
        
        self.user_update = self._user_update
        name = None
        if self.first_name:
            name = self.first_name
                
        if self.last_name:
            if name:
                name = "%s %s" % (name, self.last_name)
                
        if name:
            self.name = name
            
        super(User, self).save(*args, **kwargs)


def user_save(sender, instance, created, *args, **kwargs):
    
    if not isinstance(instance, User):
       return
    
        
post_save.connect(user_save, sender=User)



        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
