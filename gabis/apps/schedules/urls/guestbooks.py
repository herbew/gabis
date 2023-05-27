from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.schedules.views import guestbooks

urlpatterns = [
    
    path("guestbook/create/", 
        view=guestbooks.GuestBookCreateView.as_view(),
        name="guestbook_create"),
    path("guestbook/detail/", 
        view=guestbooks.GuestBookDetailListView.as_view(),
        name="guestbook_detail"),
    
    
    ]