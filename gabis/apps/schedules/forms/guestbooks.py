from __future__ import unicode_literals, absolute_import

import logging
import os
from django import forms
from django.forms.widgets import Select, TextInput, CheckboxInput

from django.conf import settings
from django.utils.safestring import mark_safe
from django.core.validators import validate_email
from django.forms.widgets import Select, TextInput
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from django.forms.widgets import NumberInput

from gabis.apps.masters.models.zones import (Keuskupan, Paroki, Wilayah, Lingkungan)
from gabis.apps.masters.models.events import TimeEvent
from gabis.apps.schedules.models.guestbooks import (
    GuestBook, SEMINAR_EVENT, ZIARAH_EVENT)

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
        self.fields['keuskupan'].queryset = Keuskupan.objects.all().order_by("ordered")
        self.fields['keuskupan'].empty_label = _("Select Keuskupan ---")
        self.fields['keuskupan'].widget.attrs.update(
                {'onchange':'paroki_on_changed()'})
        
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
        self.fields["nik"].widget = NumberInput(attrs={
            'class':"form-control text-muted",
            'type': 'number',
            'onkeypress':'return isNumberKey(event)',
            'required':''})
        
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
        
        self.fields["mobile"].widget = NumberInput(attrs={
            'class':"form-control text-muted",
            'type': 'number',
            'onkeypress':'return isNumberKey(event)',
            'required':''})
        
    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            try:
                validate_email(data)
            except:
                raise forms.ValidationError(
                    _("Enter a valid email address."))
        
        return data

        
class TokenFilterForm(forms.Form):
    
    token = forms.CharField(
        widget = TextInput(attrs={'class':'form-control text-muted', 'maxlength':255}),
        required=False
        )

    def __init__(self, *args, **kwargs):
        super(TokenFilterForm, self).__init__(*args, **kwargs)
        
        self.fields['token'].label = _("Token")
        self.fields['token'].required = False
        
        self.fields["token"].help_text = _("Input Your Token!")
        

class GuestBookFilterForm(forms.Form):
    
    params = forms.CharField(
        widget = TextInput(attrs={'class':'form-control text-muted', 'maxlength':255}),
        required=False
        )

    def __init__(self, *args, **kwargs):
        super(GuestBookFilterForm, self).__init__(*args, **kwargs)
        
        self.fields['params'].label = _("No Identitas")
        self.fields['params'].required = False
        
        self.fields["params"].help_text = _("Input Your NIK/NIS/HP Number!")
        
class GuestBookEventZiarahFilterForm(forms.Form):
    
    
    keuskupan = forms.ModelChoiceField(
        label=_("Keuskupan"),
        queryset=Keuskupan.objects.all().order_by("ordered"),
        empty_label=_("All Keuskupan ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                'onchange':'paroki_on_changed()'}),
        required=False,
    )
    
    paroki = forms.ModelChoiceField(
        label=_("Paroki"),
        queryset=Paroki.objects.all().order_by("ordered"),
        empty_label=_("All Paroki ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                'onchange':'wilayah_on_changed()'}),
        required=False,
    )
    
    wilayah = forms.ModelChoiceField(
        label=_("Wilayah"),
        queryset=Wilayah.objects.all().order_by("ordered"),
        empty_label=_("All Wilayah ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                'onchange':'lingkungan_on_changed()'}),
        required=False,
    )
    
    lingkungan = forms.ModelChoiceField(
        label=_("Lingkungan"),
        queryset=Lingkungan.objects.all().order_by("ordered"),
        empty_label=_("All Lingkungan ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                }),
        required=False,
    )
    
    
    attended = forms.BooleanField(
        label=_("Is Attended"),
        widget=forms.CheckboxInput(attrs={
                'class':'form-control checkbox text-muted',
                }),
        required=False,
        )
    
    kloter = forms.ModelChoiceField(
        label=_("Kloter"),
        queryset=TimeEvent.objects.filter(event__name=ZIARAH_EVENT).order_by("ordered"),
        empty_label=_("All Kloter ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted'}),
        required=False,
    )
    
    params = forms.CharField(
        widget = TextInput(attrs={'class':'form-control text-muted', 'maxlength':255}),
        required=False
        )

    def __init__(self, *args, **kwargs):
        super(GuestBookEventZiarahFilterForm, self).__init__(*args, **kwargs)
        
        self.fields['params'].label = _("No Identitas/Name/Token")
        self.fields['params'].required = False
        
        self.fields["params"].help_text = _("Input Your Name, NIK/NIS/HP Number, or Token!")
        
        

class GuestBookEventSeminarFilterForm(forms.Form):
    
    
    keuskupan = forms.ModelChoiceField(
        label=_("Keuskupan"),
        queryset=Keuskupan.objects.all().order_by("ordered"),
        empty_label=_("All Keuskupan ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                'onchange':'paroki_on_changed()'}),
        required=False,
    )
    
    paroki = forms.ModelChoiceField(
        label=_("Paroki"),
        queryset=Paroki.objects.all().order_by("ordered"),
        empty_label=_("All Paroki ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                'onchange':'wilayah_on_changed()'}),
        required=False,
    )
    
    wilayah = forms.ModelChoiceField(
        label=_("Wilayah"),
        queryset=Wilayah.objects.all().order_by("ordered"),
        empty_label=_("All Wilayah ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                'onchange':'lingkungan_on_changed()'}),
        required=False,
    )
    
    lingkungan = forms.ModelChoiceField(
        label=_("Lingkungan"),
        queryset=Lingkungan.objects.all().order_by("ordered"),
        empty_label=_("All Lingkungan ---"),
        widget=forms.Select(attrs={
                'class':'form-control text-muted',
                }),
        required=False,
    )
    
    
    paid = forms.BooleanField(
        label=_("Is Paid"),
        widget=forms.CheckboxInput(attrs={
                'class':'form-control checkbox text-muted',
                }),
        required=False,
        )
    
    attended = forms.BooleanField(
        label=_("Is Attended"),
        widget=forms.CheckboxInput(attrs={
                'class':'form-control checkbox text-muted',
                }),
        required=False,
        )
    
    params = forms.CharField(
        widget = TextInput(attrs={'class':'form-control text-muted', 'maxlength':255}),
        required=False
        )

    def __init__(self, *args, **kwargs):
        super(GuestBookEventSeminarFilterForm, self).__init__(*args, **kwargs)
        
        self.fields['params'].label = _("No Identitas/Name/Token")
        self.fields['params'].required = False
        
        self.fields["params"].help_text = _("Input Your Name, NIK/NIS/HP Number, or Token!")
        
        
        
        
        