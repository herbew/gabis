# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse, reverse_lazy
from django.views.generic import RedirectView
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from gabis.apps.users.models.users import User



class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        if self.request.user.types in ('001',):
            # return reverse_lazy("staffs:master_company_list")
            return reverse_lazy("schedules:time_event_ziarah_list")
        
        logout(self.request)
        # return reverse_lazy("account_login")
        return reverse_lazy("schedules:time_event_ziarah_list")
        
redirect = UserRedirectView.as_view()

class SignUpRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        list(messages.get_messages(self.request))
        messages.success(
            self.request, 
            _("Have successfully registered.") 
            )
        logout(self.request)
        # return reverse_lazy("account_login")
        return reverse_lazy("schedules:time_event_ziarah_list")
        
signup_redirect = SignUpRedirectView.as_view()


class UserSigninView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        if self.request.user.types in ('001',):
            # return reverse_lazy("staffs:master_company_list")
            return reverse_lazy("schedules:time_event_ziarah_list")
        
        logout(self.request)
        return reverse_lazy("account_login")
        
login_redirect = UserSigninView.as_view()



