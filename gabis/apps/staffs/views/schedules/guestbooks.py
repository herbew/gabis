from __future__ import unicode_literals, absolute_import

import logging

from django.urls import reverse, reverse_lazy

from gabis.apps.users.viewmixins.roles import AdminMixin

from gabis.apps.schedules.views.guestbooks import (
    GuestBookDetailListView as MasterGuestBookDetailListView,
    AttendGuestView as MasterAttendGuestView
    )

log = logging.getLogger(__name__)
class GuestBookDetailListView(AdminMixin, MasterGuestBookDetailListView):
    template_name = "staffs/schedules/bookings/guestbooks/detail.html"
        
class AttendGuestView(AdminMixin, MasterAttendGuestView):
    def get_success_url(self):
        
        obj = self.get_object()
        
        url = reverse_lazy("staffs:guestbook_detail")
        return dict(status=200, url="%s?params=%s" % (url, obj.id))