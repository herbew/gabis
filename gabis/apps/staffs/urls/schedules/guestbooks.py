from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.staffs.views.schedules import guestbooks

urlpatterns = [
    
    path("guestbook/detail/", 
        view=guestbooks.GuestBookDetailListView.as_view(),
        name="guestbook_detail"),
    path("guestbook/<int:pk_guest_book>/attended/", 
        view=guestbooks.AttendGuestView.as_view(),
        name="guestbook_attended"),
    
    ]