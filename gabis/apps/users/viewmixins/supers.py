# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.http import Http404
from braces.views import UserPassesTestMixin
from gabis.core.choices import USER_CHOICES


class AdminMixin(UserPassesTestMixin):
    """Admin"""
    
    raise_exception = Http404
    def get_context_data(self, **kwargs):
        context = super(AdminMixin, self).get_context_data(**kwargs)
        
        return context
    
    def test_func(self, user):
        """
        Check if request user should access types or not.
        """
        if user.types == '001' :
                return True
       
        return False
    

