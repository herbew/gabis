# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from gabis.apps.schedules.urls.bookings import urlpatterns as bookings_urlpatterns
from gabis.apps.schedules.urls.guestbooks import urlpatterns as guestbooks_urlpatterns

app_name = "schedules"

urlpatterns = bookings_urlpatterns
urlpatterns += guestbooks_urlpatterns