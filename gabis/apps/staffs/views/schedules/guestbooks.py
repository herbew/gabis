from __future__ import unicode_literals, absolute_import

import logging

from django.urls import reverse, reverse_lazy

from gabis.apps.users.viewmixins.roles import AdminMixin, CSMixin

from gabis.apps.schedules.views.guestbooks import (
    GuestBookDetailListView as MasterGuestBookDetailListView,
    AttendGuestView as MasterAttendGuestView,
    PayGuestView as MasterPayGuestView,
    GuestBookListView as MasterGuestBookListView,
    DeleteGuestView as MasterDeleteGuestView,
    GuestBookSeminarPrintView as MasterGuestBookSeminarPrintView,
    GuestBookZiarahPrintView as MasterGuestBookZiarahPrintView
    
    )

SEMINAR_EVENT = "Seminar Kain Kafan Yesus 2023"
ZIARAH_EVENT = "Ziarah Kain Kafan Yesus 2023"

log = logging.getLogger(__name__)
class GuestBookDetailListView(CSMixin, MasterGuestBookDetailListView):
    template_name = "staffs/schedules/bookings/guestbooks/detail.html"
        
class AttendGuestView(CSMixin, MasterAttendGuestView):
    def get_success_url(self):
        
        obj = self.get_object()
        
        url = reverse_lazy("staffs:guestbook_detail")
        return dict(status=200, url="%s?params=%s" % (url, obj.id))
    
class PayGuestView(AdminMixin, MasterPayGuestView):
    def get_success_url(self):
        
        obj = self.get_object()
        
        url = reverse_lazy("staffs:guestbook_detail")
        return dict(status=200, url="%s?params=%s" % (url, obj.id))
    
    
class GuestBookZiarahListView(CSMixin, MasterGuestBookListView):
    template_name = "staffs/schedules/bookings/guestbooks/ziarah_list.html"
    
class GuestBookSeminarListView(CSMixin, MasterGuestBookListView):
    template_name = "staffs/schedules/bookings/guestbooks/seminar_list.html"
    
class DeleteGuestView(AdminMixin, MasterDeleteGuestView):
    def get_success_url(self):
        
        if self.event == SEMINAR_EVENT:
            url = reverse_lazy("staffs:guestbook_seminar_list")
        else:
            url = reverse_lazy("staffs:guestbook_ziarah_list")
        
        return dict(status=200, url=url)


class GuestBookSeminarPrintView(AdminMixin, MasterGuestBookSeminarPrintView):
    pass

class GuestBookZiarahPrintView(AdminMixin, MasterGuestBookZiarahPrintView):
    pass
    