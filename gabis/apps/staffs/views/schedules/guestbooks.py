from __future__ import unicode_literals, absolute_import

import logging

from django.urls import reverse, reverse_lazy

from gabis.apps.users.viewmixins.roles import AdminMixin

from gabis.apps.schedules.views.guestbooks import (
    GuestBookDetailListView as MasterGuestBookDetailListView
    )

log = logging.getLogger(__name__)
class GuestBookDetailListView(AdminMixin, MasterGuestBookDetailListView):
    template_name = "staffs/schedules/bookings/guestbooks/detail.html"
        
