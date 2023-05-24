from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.schedules.views import bookings 

urlpatterns = [
        path("time/event/ziarah/list/", 
        view=bookings.TimeEventZiarahListView.as_view(),
        name="time_event_ziarah_list"),
        
        ]