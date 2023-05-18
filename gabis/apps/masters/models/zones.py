# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.db import models

from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete

from django_extensions.db.models import TimeStampedModel

log = logging.getLogger(__name__)


class Keuskupan(TimeStampedModel):
    """Keuskupan"""
    name = models.CharField(
        _("Name"), unique=True, max_length=100, db_index=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"Keuskupan"
        verbose_name_plural = u"001001 Keuskupan"

    def __init__(self, *args, **kwargs):
        super(Keuskupan, self).__init__(*args, **kwargs)
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
        super(Keuskupan, self).save(*args, **kwargs)


class Paroki(TimeStampedModel):
    """Paroki"""
    
    keuskupan = models.ForeignKey(Keuskupan,
                on_delete=models.CASCADE,
                verbose_name=_("Keuskupan"),
                db_index=True, null=True, blank=True)
    
    name = models.CharField(
        _("Name"), max_length=255, db_index=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"Paroki"
        verbose_name_plural = u"001002 Paroki"
        unique_together = (("keuskupan", "name",),)

    def __init__(self, *args, **kwargs):
        super(Paroki, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s %s" % (self.keuskupan, self.name)
    

    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Paroki, self).save(*args, **kwargs)
        

class Wilayah(TimeStampedModel):
    """Wilayah"""
    
    paroki = models.ForeignKey(Paroki,
                on_delete=models.CASCADE,
                verbose_name=_("Paroki"),
                db_index=True, null=True, blank=True)
    
    name = models.CharField(
        _("Name"), max_length=255, db_index=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"Wilayah"
        verbose_name_plural = u"001003 Wilayah"
        unique_together = (("paroki", "name",),)

    def __init__(self, *args, **kwargs):
        super(Wilayah, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s %s" % (self.paroki, self.name)
    

    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Wilayah, self).save(*args, **kwargs)
        
        
        
class Lingkungan(TimeStampedModel):
    """Lingkungan"""
    
    wilayah = models.ForeignKey(Wilayah,
                on_delete=models.CASCADE,
                verbose_name=_("Wilayah"),
                db_index=True, null=True, blank=True)
    
    name = models.CharField(
        _("Name"), max_length=255, db_index=True)
    
    user_update = models.CharField(
            max_length=30,
            blank=True, null=True,
            db_index=True)

    class Meta:
        app_label = 'masters'
        verbose_name = u"Lingkungan"
        verbose_name_plural = u"001004 Lingkungan"
        unique_together = (("wilayah", "name",),)

    def __init__(self, *args, **kwargs):
        super(Lingkungan, self).__init__(*args, **kwargs)
        self._user_update = None

    def __str__(self):
        return "%s %s" % (self.wilayah, self.name)
    

    def get_user_update(self):
        return self._user_update

    def set_user_update(self, new_user):
        self._user_update = new_user

    user_updated = property(get_user_update, set_user_update, None, "user_updated")

    def save(self, *args, **kwargs):
        self.user_update = self._user_update
        super(Lingkungan, self).save(*args, **kwargs)
