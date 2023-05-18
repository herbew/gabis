from __future__ import unicode_literals, absolute_import

import logging

from django.core.paginator import EmptyPage, Paginator

log = logging.getLogger(__name__)

class SafePaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(SafePaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise