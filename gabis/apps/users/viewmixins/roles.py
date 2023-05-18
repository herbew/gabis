# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.http import Http404
from django.contrib.auth.mixins import UserPassesTestMixin

from gabis.core.choices import USER_CHOICES
from gabis.apps.users.models.users import User


class AdminMixin(UserPassesTestMixin):
    """Admin"""
    
    raise_exception = Http404
    
    def get_context_data(self, **kwargs):
        context = super(AdminMixin, self).get_context_data(**kwargs)
        
        return context
    
    def test_func(self):
        """
        Check if request user should access types or not.
        """
        if self.request.user.types == '001' :
            return True
       
        return False
    
class ClientMixin(UserPassesTestMixin):
    """Client"""
    
    raise_exception = Http404
    
    def get_context_data(self, **kwargs):
        context = super(ClientMixin, self).get_context_data(**kwargs)
        
        return context
    
    def test_func(self):
        """
        Check if request user should access types or not.
        """
        
        if self.request.user.types == '002' :
            return True
       
        return False
    
        
