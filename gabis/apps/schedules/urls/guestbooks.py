from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.schedules.views import guestbooks

urlpatterns = [
    
    path("guestbook/<int:pk_time_event>/create/", 
        view=guestbooks.GuestBookCreateView.as_view(),
        name="guestbook_create"),
    
    
    
    ]