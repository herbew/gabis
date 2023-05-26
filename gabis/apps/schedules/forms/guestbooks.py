from __future__ import unicode_literals, absolute_import

import logging
import os
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.validators import validate_email
from django.forms.widgets import Select, TextInput
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from gabis.apps.schedules.models.guestbooks import GuestBook

log = logging.getLogger(__name__)

class GuestBookForm(forms.ModelForm):

    class Meta:
        model = GuestBook
        fields = ('keuskupan','paroki','wilayah','lingkungan',
                  'nik','name','gender','age','mobile','email')
    
    def __init__(self, *args, **kwargs):
        super(GuestBookForm, self).__init__(*args, **kwargs)
        
        for field in self.Meta.fields:
        
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
                
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
        
        self.fields["keuskupan"].label = _("Keuskupan")
        self.fields["keuskupan"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['keuskupan'].label)
        self.fields['keuskupan'].empty_label = _("Select Keuskupan ---")
        self.fields['keuskupan'].widget.attrs.update(
                {'onchange':'paroki_on_change()'})
        
        self.fields["paroki"].label = _("Paroki")
        self.fields["paroki"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['paroki'].label)
        self.fields['paroki'].empty_label = _("Select Paroki ---")
        
        self.fields["wilayah"].label = _("Wilayah")
        self.fields["wilayah"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['wilayah'].label)
        self.fields['wilayah'].empty_label = _("Select Wilayah ---")
        
        self.fields["lingkungan"].label = _("Lingkungan")
        self.fields["lingkungan"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['lingkungan'].label)
        
        self.fields["nik"].label = _("Identity Number")
        self.fields["nik"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['nik'].label)
        self.fields["nik"].help_text = _("NIK or NIS or Mobile Phone Number!")
        self.fields["nik"].widget.attrs.update({'onkeypress':'return isNumberKey(event)'})
        
        
        self.fields["name"].label = _("Name")
        self.fields["name"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['name'].label)
        
        self.fields["gender"].label = _("Gender")
        self.fields["gender"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['gender'].label)
        self.fields['gender'].choices = (
                tuple([("",_("Select Gender ---"))] + 
                list(GuestBook.GENDER_CHOICES)))
        
        self.fields["age"].label = _("Age")
        self.fields["age"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['age'].label)
        self.fields["age"].widget.attrs.update({'onkeypress':'return isNumberKey(event)'})
        
        self.fields["mobile"].label = _("Mobile Number")
        self.fields["mobile"].label =  mark_safe(
                        "%s <font color=red size=4.5em>*</font>" % 
                        self.fields['mobile'].label)
        
    def clean_email(self):
        data = self.cleaned_data['email']
        try:
            validate_email(data)
        except:
            raise forms.ValidationError(
                _("Enter a valid email address."))
        
        return data

        
        
        
        
        
        
        
        
        