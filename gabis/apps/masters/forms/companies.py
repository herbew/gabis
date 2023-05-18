from __future__ import unicode_literals, absolute_import

import logging

from django import forms
from django.utils.safestring import mark_safe
from django.forms.widgets import Select, TextInput, CheckboxInput
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

from collections import OrderedDict

from gabis.apps.masters.models.companies import (Company, PICCompany)
from gabis.apps.users.models.users import User

log = logging.getLogger(__name__)

MAX_LOGO_UPLOAD_SIZE = int(500*1024)


class CompanyForm(forms.ModelForm):
    
    class Meta:
        model = Company
        fields = ('name','types', 'address','logo', 'email', 'phone','fax')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
        
        self.fields['name'].label = _("Name")
        self.fields['name'].label =  mark_safe(
            "%s <font color=red size=4.5em>*</font>" % self.fields['name'].label) 
        
        self.fields['types'].choices = tuple(
                    [("",_("Select Company Type  ---"))] + 
                    list(Company.TYPES_CHOICES)
                )
        
        self.fields['types'].required = True
        self.fields['types'].label =  mark_safe(
            "%s <font color=red size=4.5em>*</font>" % self.fields['types'].label) 
        
        self.fields['address'].help_text = _("Address, max 1.0 MB.")
        
        self.fields['logo'].help_text = _("Image, max 500 KBytes.")
        self.fields['logo'].widget.attrs.update(
                        {'accept':"image/*"}
                        )
        
        
    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            try:
                validate_email(data)
            except:
                raise forms.ValidationError(_("Enter a valid email address."))
        
        return data
    
    def clean_address(self):
        
        FILE_SIZE = int(2 * MAX_LOGO_UPLOAD_SIZE)
        
        data = self.cleaned_data['address']
        if data:
            if len(data.encode('utf-8')) > FILE_SIZE:
                 raise forms.ValidationError(_('Make sure the Address size is under %s. Now %s') % (
                     filesizeformat(FILE_SIZE), filesizeformat(len(data.encode('utf-8')))))
        
        return data
    
    
    def clean_logo(self):
        
        data = self.cleaned_data['logo']
        
        if data:
            try:
                if int(data.size) > MAX_LOGO_UPLOAD_SIZE:
                 raise forms.ValidationError(_('Make sure the attachment file size is under %s. Now %s') % (
                     filesizeformat(MAX_LOGO_UPLOAD_SIZE), filesizeformat(data.size)))
            except:
                pass
            
        return data


class CompanyFilterForm(forms.Form):
    cname = forms.CharField(
        label=_("Company Name"),
        widget=TextInput(attrs={'class':'form-control text-muted'}),
        required=False
    )
    
    
class PICCompanyForm(forms.ModelForm):
    username = forms.CharField(max_length=30,
        widget = TextInput(attrs={
            'class':'form-control text-muted',
            }),
        required=True
    )
    
    name = forms.CharField(max_length=250,
        widget = TextInput(attrs={
            'class':'form-control text-muted',
            }),
        required=True
    )
    
    gender = forms.CharField(
        widget = Select(attrs={'class':'form-control text-muted',},
                        choices=tuple([('',_('Select Gender ---'))] + \
                                list(User.GENDER_CHOICES)))
    )
    
    password1 = forms.CharField(
        widget = TextInput(attrs={'class':'form-control text-muted',
                                  'type': 'password'}),
        required=True
    )
    
    password2 = forms.CharField(
        widget = TextInput(attrs={'class':'form-control text-muted',
                                  'type': 'password'}),
        required=True
    )
    
    class Meta:
        model = PICCompany
        fields = ('position', 'email', 'phone', 'ext', 'mobile')

    def __init__(self, *args, **kwargs):
        super(PICCompanyForm, self).__init__(*args, **kwargs)
        
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
        
       
        self.fields['username'].label = _("Username")
        self.fields['username'].widget = forms.TextInput(
            attrs={'class':'form-control text-muted','autofocus': 'autofocus'})
        self.fields['username'].label = mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['username'].label)
        self.fields['username'].help_text = _("Required. Min 8 to 30 characters or fewer. Letters, digits and @/./+/-/_ only.")
        
        self.fields['email'].label = _("Email") 
        self.fields['email'].required = True
        self.fields['email'].label = mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['email'].label)
        
        self.fields['name'].label = _("Name")
        self.fields['name'].label = mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['name'].label)
        
        self.fields['password1'].label = _("Password")
        self.fields['password1'].label = mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['password1'].label)
        
        self.fields['password2'].label = _("Password (again)")
        self.fields['password2'].label = mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['password2'].label)
        
        self.fields['ext'].widget.attrs.update(
            {'class':'form-control',
             'onkeypress':'return isNumberKey(event)',
            'type':'text'})
        
        
        new_fields = OrderedDict()
        
        new_fields['username'] = self.fields['username']
        new_fields['email'] = self.fields['email']
        new_fields['name'] = self.fields['name']
        new_fields['password1'] = self.fields['password1']
        new_fields['password2'] = self.fields['password2']
        new_fields['gender'] = self.fields['gender']
        new_fields['position'] = self.fields['position']
        new_fields['phone'] = self.fields['phone']
        new_fields['ext'] = self.fields['ext']
        new_fields['mobile'] = self.fields['mobile']
        
        self.fields = new_fields
        
        
        
    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            validate_email(data)
        except:
            raise forms.ValidationError(_("Enter a valid email address."))
        
        user = User.objects.filter(email=data)
            
        if user:
            raise forms.ValidationError(_("The Email already exists"))
        
        return data
    
    def clean_password1(self):
        data = self.cleaned_data['password1']
        if len(data) < 8 or len(data) > 30:
            raise forms.ValidationError( _("Required. Min 8 to 30 characters or fewer. Letters, digits and @/./+/-/_ only."))
        return data
    
    def clean_password2(self):
        data = self.cleaned_data['password2']
        return data
    
    def clean_username(self):
        data = self.cleaned_data['username']
        
        
        user = User.objects.filter(username=data)
        
        if user:
            raise forms.ValidationError(_("The Username already exists"))
        
        return data
        
    def clean(self):
        cleaned_data = super(PICCompanyForm,self).clean()
        
        password1 = None
        password2 = None
        
        if 'password1' in cleaned_data:
            password1 = cleaned_data.get('password1')
            
        if 'password2' in cleaned_data:
            password1 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError( _("You must type the same password each time."))
        
        return cleaned_data
    
class UpdatePICCompanyForm(forms.ModelForm):
    
    name = forms.CharField(max_length=250,
        widget = TextInput(attrs={
            'class':'form-control text-muted',
            }),
        required=True
    )
    
    gender = forms.CharField(
        widget = Select(attrs={'class':'form-control text-muted',},
                        choices=tuple([('',_('Select Gender ---'))] + \
                                list(User.GENDER_CHOICES)))
    )
    
    
    class Meta:
        model = PICCompany
        fields = ('position', 'email', 'phone', 'ext', 'mobile')

    def __init__(self, *args, **kwargs):
        super(UpdatePICCompanyForm, self).__init__(*args, **kwargs)
        
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
        
        self.fields['email'].label = _("Email") 
        self.fields['email'].required = True
        self.fields['email'].label = mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['email'].label)
        
        self.fields['name'].label = _("Name")
        self.fields['name'].label = mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['name'].label)
        
        self.fields['ext'].widget.attrs.update(
            {'class':'form-control',
             'onkeypress':'return isNumberKey(event)',
            'type':'text'})
        
        
        new_fields = OrderedDict()
        
        new_fields['email'] = self.fields['email']
        new_fields['name'] = self.fields['name']
        new_fields['gender'] = self.fields['gender']
        new_fields['position'] = self.fields['position']
        new_fields['phone'] = self.fields['phone']
        new_fields['ext'] = self.fields['ext']
        new_fields['mobile'] = self.fields['mobile']
        
        self.fields = new_fields
        
        
        
    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            validate_email(data)
        except:
            raise forms.ValidationError(_("Enter a valid email address."))
        
        user = User.objects.filter(email=data).exclude(id=self.instance.pic.id)
            
        if user:
            raise forms.ValidationError(_("The Email already exists"))
        
        return data
    


class PICCompanyFilterForm(forms.Form):
    
    company = forms.ModelChoiceField(
            label=_("Company"),
            queryset = Company.objects.all(),
            empty_label = _("All Companies ---"),
            widget = forms.Select(attrs={'class':'form-control text-muted'},),
            required=False
    )
    
    pic_name = forms.CharField(
        label=_("PIC Name"),
        widget = TextInput(attrs={'class':'form-control text-muted'}),
        required=False
    )  
    

    
    
    
    
    
    
    
    
    
    
