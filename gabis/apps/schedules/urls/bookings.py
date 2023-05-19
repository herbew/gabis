from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.schedules.views import bookings 

urlpatterns = [
        path("time/event/list/", 
        view=bookings.TimeEventListView.as_view(),
        name="time_event_list"),
        
        ]