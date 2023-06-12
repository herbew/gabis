from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.staffs.views.schedules import guestbooks

urlpatterns = [
    
    path("guestbook/detail/", 
        view=guestbooks.GuestBookDetailListView.as_view(),
        name="guestbook_detail"),
    path("guestbook/<int:pk_guest_book>/attend/", 
        view=guestbooks.AttendGuestView.as_view(),
        name="guestbook_attended"),
    path("guestbook/<int:pk_guest_book>/pay/", 
        view=guestbooks.PayGuestView.as_view(),
        name="guestbook_paid"),
    
    path("guestbook/ziarah/list/", 
        view=guestbooks.GuestBookZiarahListView.as_view(),
        kwargs=dict(filter_event=1),
        name="guestbook_ziarah_list"),
    
    path("guestbook/seminar/list/", 
        view=guestbooks.GuestBookSeminarListView.as_view(),
        kwargs=dict(filter_event=2),
        name="guestbook_seminar_list"),
    
    path("guestbook/<int:pk_guest_book>/delete/", 
        view=guestbooks.DeleteGuestView.as_view(),
        name="guestbook_deleted"),
    
    path("guestbook/seminar/print/", 
        view=guestbooks.GuestBookSeminarPrintView.as_view(),
        name="guestbook_seminar_print"),
    
    path("guestbook/ziarah/print/", 
        view=guestbooks.GuestBookZiarahPrintView.as_view(),
        name="guestbook_ziarah_print"),
     
    ]