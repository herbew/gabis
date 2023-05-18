# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from gabis.apps.schedules.models.bookings import BookingTimeEvent
from gabis.apps.schedules.models.guestbooks import GuestBook

admin.site.register(BookingTimeEvent)
admin.site.register(GuestBook)
