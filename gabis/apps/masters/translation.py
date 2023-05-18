from __future__ import unicode_literals, absolute_import

import logging

from modeltranslation.translator import translator, TranslationOptions

from gabis.apps.masters.models.zones import (Keuskupan, Paroki, Wilayah, Lingkungan)
from gabis.apps.masters.models.events import (Event, TimeEvent, PICEvent)


log = logging.getLogger(__name__)

class KeuskupanTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Keuskupan, KeuskupanTranslationOptions)

class ParokiTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Paroki, ParokiTranslationOptions)

class WilayahTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Wilayah, WilayahTranslationOptions)

class LingkunganTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Lingkungan, LingkunganTranslationOptions)

class EventTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Event, EventTranslationOptions)

class TimeEventTranslationOptions(TranslationOptions):
    fields = ('start_time','end_time','max_guest')

translator.register(TimeEvent, TimeEventTranslationOptions)

class PICEventTranslationOptions(TranslationOptions):
    fields = ('position','email','mobile')

translator.register(PICEvent, PICEventTranslationOptions)
