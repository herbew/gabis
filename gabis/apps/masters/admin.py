# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from gabis.apps.masters.models.zones import (Keuskupan, Paroki, Wilayah, Lingkungan)
from gabis.apps.masters.models.events import (Event, TimeEvent, PICEvent)



admin.site.register(Keuskupan)
admin.site.register(Paroki)
admin.site.register(Wilayah)
admin.site.register(Lingkungan)

admin.site.register(Event)
admin.site.register(TimeEvent)
admin.site.register(PICEvent)

