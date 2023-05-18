from __future__ import unicode_literals, absolute_import

import re

from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.utils import perform_login
from allauth.account import app_settings
from allauth.account.models import EmailAddress
from allauth.account.forms import (
    SignupForm as AllAuthSignupForm, 
    LoginForm as AllAuthLoginForm,
    ChangePasswordForm as AllAuthChangePasswordForm,
    SetPasswordForm as AllAuthSetPasswordForm,
    ResetPasswordKeyForm as AllAuthResetPasswordKeyForm,
    )


class SignupForm(AllAuthSignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget = forms.TextInput(
            attrs={'type': 'email', 'autofocus': 'autofocus'})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'type': 'password'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'type': 'password'})
            
    def clean_password1(self):
        
        data = self.cleaned_data['password1']
        
        m = re.match(r'^(?=[^A-Z]*[A-Z])(?=[^0-9]*[0-9])', data)
        
        if not m:
            raise forms.ValidationError(
                    _("Please input min one Upper Character and any number!"))
        
        return data   

class LoginForm(AllAuthLoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
                    
        self.fields['password'].label = ""
        self.fields['login'].label = ""
        self.fields['remember'].widget = forms.HiddenInput()
    
    def login(self, request, redirect_url=None):
        ea = EmailAddress.objects.get(user=self.user)
        ea.set_as_primary()
        ea.verified = True
        ea.save()
            
        email = ea.email #self.user_credentials().get("email")
        
        try:
            ret = perform_login(
                request,
                self.user,
                email_verification=app_settings.EMAIL_VERIFICATION,
                redirect_url=redirect_url,
                email=email,
            )
        except:
            ret = perform_login(
                request,
                self.user,
                email_verification=app_settings.EMAIL_VERIFICATION,
                redirect_url=redirect_url
            )
        
        remember = app_settings.SESSION_REMEMBER
        if remember is None:
            remember = self.cleaned_data["remember"]
        
        if remember:
            request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        
        return ret
    
        
class ChangePasswordForm(AllAuthChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
            
    def clean_password1(self):
        
        data = self.cleaned_data['password1']
        
        m = re.match(r'^(?=[^A-Z]*[A-Z])(?=[^0-9]*[0-9])', data)
        
        if not m:
            raise forms.ValidationError(
                    _("Please input min one Upper Character and any number!"))
        
        return data   
  
class SetPasswordForm(AllAuthSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
            
    def clean_password1(self):
        
        data = self.cleaned_data['password1']
        
        m = re.match(r'^(?=[^A-Z]*[A-Z])(?=[^0-9]*[0-9])', data)
        
        if not m:
            raise forms.ValidationError(
                    _("Please input min one Upper Character and any number!"))
        
        return data   
        
class ResetPasswordKeyForm(AllAuthResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
        
            
    def clean_password1(self):
        
        data = self.cleaned_data['password1']
        
        m = re.match(r'^(?=[^A-Z]*[A-Z])(?=[^0-9]*[0-9])', data)
        
        if not m:
            raise forms.ValidationError(
                    _("Please input min one Upper Character and any number!"))
        
        return data   
