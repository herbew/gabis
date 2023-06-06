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
    path("guestbook/<int:pk_guest_book>/paid/", 
        view=guestbooks.PayGuestView.as_view(),
        name="guestbook_paid"),
    
    path("guestbook/ziarah/list/", 
        view=guestbooks.GuestBookZiarahListView.as_view(),
        kwargs=dict(filter_event=1),
        name="guestbook_ziarah_list"),
    
    path("guestbook/seminar/list/", 
        view=guestbooks.GuestBookZiarahListView.as_view(),
        kwargs=dict(filter_event=2),
        name="guestbook_seminar_list"),
    ]