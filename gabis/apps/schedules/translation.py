from __future__ import unicode_literals, absolute_import

import logging

from modeltranslation.translator import translator, TranslationOptions
from gabis.apps.schedules.models.bookings import BookingTimeEvent
from gabis.apps.schedules.models.guestbooks import GuestBook

log = logging.getLogger(__name__)

class BookingTimeEventTranslationOptions(TranslationOptions):
    fields = ('group','pic_group','email','mobile' )

translator.register(BookingTimeEvent, BookingTimeEventTranslationOptions)


class GuestBookTranslationOptions(TranslationOptions):
    fields = ('name','age','email','mobile' )

translator.register(GuestBook, GuestBookTranslationOptions)
