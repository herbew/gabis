from __future__ import unicode_literals, absolute_import

import logging

from django import forms
from django.utils.safestring import mark_safe
from django.forms.widgets import Select, TextInput, CheckboxInput
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

from collections import OrderedDict

from gabis.apps.localized.models.zones import (
    Country, Zone, TimeZone
    )
from gabis.apps.masters.models.companies import Company
from gabis.apps.masters.models.buildings import (Building, Room)

log = logging.getLogger(__name__)

MAX_IMAGE_UPLOAD_SIZE = int(500*1024)


class BuildingForm(forms.ModelForm):
     
    class Meta:
        model = Building
        fields = (
                'company', 'name', 'address', 
                'email', 'image', 'ordered')

    def __init__(self, *args, **kwargs):
        super(BuildingForm, self).__init__(*args, **kwargs)
        
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
        
        self.fields['company'].label = _("Company")
        self.fields['company'].empty_label = _("Select Company ---")
        self.fields['company'].queryset = Company.objects.all().order_by("name")
        self.fields['company'].label =  mark_safe(
            "%s <font color=red size=4.5em>*</font>" % self.fields['company'].label) 
        
        self.fields['name'].label = _("Name")
        self.fields['name'].label =  mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['name'].label) 
        
        self.fields['address'].help_text = _("Address, max 1.0 MB.")
        
        self.fields['image'].help_text = _("Image, max 500 KBytes.")
        self.fields['image'].widget.attrs.update(
                        {'accept':"image/*"}
                        )
        
        self.fields['ordered'].label =  mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['ordered'].label) 
        
        self.fields['ordered'].widget.attrs.update(
            {'class':'form-control',
             'onkeypress':'return isNumberKey(event)',
            'type':'text'})
        
    def clean_email(self):
        data = self.cleaned_data['email']
        if data:
            try:
                validate_email(data)
            except:
                raise forms.ValidationError(_("Enter a valid email address."))
        
        return data
    
    def clean_address(self):
        
        FILE_SIZE = int(2 * MAX_IMAGE_UPLOAD_SIZE)
        
        data = self.cleaned_data['address']
        if data:
            if len(data.encode('utf-8')) > FILE_SIZE:
                 raise forms.ValidationError(_('Make sure the Address size is under %s. Now %s') % (
                     filesizeformat(FILE_SIZE), filesizeformat(len(data.encode('utf-8')))))
        
        return data
    
    
    def clean_image(self):
        
        data = self.cleaned_data['image']
        
        if data:
            try:
                if int(data.size) > MAX_IMAGE_UPLOAD_SIZE:
                 raise forms.ValidationError(_('Make sure the attachment file size is under %s. Now %s') % (
                     filesizeformat(MAX_IMAGE_UPLOAD_SIZE), filesizeformat(data.size)))
            except:
                pass
            
        return data

class BuildingFilterForm(forms.Form):
    company = forms.ModelChoiceField(
            label=_("Company"),
            queryset = Company.objects.all().order_by("name"),
            empty_label = _("All Companies ---"),
            widget = forms.Select(attrs={'class':'form-control text-muted'},),
            required=False
    )
    
    building = forms.CharField(
        label=_("Building Name"),
        widget = TextInput(attrs={'class':'form-control'}),
        required=False
    )
    
class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ( 'name', 'ext', 'image', 'desc', 'capacity','ordered')

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
            try:
                self.fields[field].widget.attrs.update(
                {'maxlength':'%s' % (self.fields[field].max_length,)})
            except:
                continue
        
        self.fields['name'].label = _("Name")
        self.fields['name'].label =  mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['name'].label) 
        
        self.fields['desc'].help_text = _("Description, max 1.0 MB.")
        self.fields['image'].help_text = _("Image, max 500 KBytes.")
        
        
        self.fields['ext'].widget.attrs.update(
            {'class':'form-control',
             'onkeypress':'return isNumberKey(event)',
            'type':'text'})
        
        self.fields['capacity'].widget.attrs.update(
            {'class':'form-control',
             'onkeypress':'return isNumberKey(event)',
            'type':'text'})
        
        self.fields['capacity'].label =  mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['capacity'].label) 
        self.fields['ordered'].required = True
        self.fields['ordered'].label =  mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['ordered'].label) 
        
    def clean_desc(self):
        
        FILE_SIZE = int(2 * MAX_IMAGE_UPLOAD_SIZE)
        
        data = self.cleaned_data['desc']
        if data:
            if len(data.encode('utf-8')) > FILE_SIZE:
                 raise forms.ValidationError(_('Make sure the Description size is under %s. Now %s') % (
                     filesizeformat(FILE_SIZE), filesizeformat(len(data.encode('utf-8')))))
        
        return data
    
    def clean_image(self):
        
        data = self.cleaned_data['image']
        
        if data:
            try:
                if int(data.size) > MAX_IMAGE_UPLOAD_SIZE:
                 raise forms.ValidationError(_('Make sure the attachment file size is under %s. Now %s') % (
                     filesizeformat(MAX_IMAGE_UPLOAD_SIZE), filesizeformat(data.size)))
            except:
                pass
            
        return data
    
    def clean(self):
        cleaned_data = super(RoomForm, self).clean()
        
        name = cleaned_data['name']
        
        if self.instance.id:
            building = self.instance.building
            room = Room.objects.filter(building=building, name=name).exclude(pk=self.instance.id)
        
            if room:
                raise forms.ValidationError(_("The name of Room already exists"))
        
        return cleaned_data

class RoomFilterForm(forms.Form):
    
    room = forms.CharField(
        label=_("Room Name"),
        widget = TextInput(attrs={'class':'form-control text-muted'}),
        required=False
    )  
    

    
    
    

# class BuildingForm(forms.ModelForm):
#
#     class Meta:
#         model = Building
#         fields = (
#                 'country','zone',
#                 'time_zone', 'company', 'name', 'address', 
#                 'email', 'image', 'ordered')
#
#     def __init__(self, *args, **kwargs):
#         super(BuildingForm, self).__init__(*args, **kwargs)
#
#         for field in self.Meta.fields:
#             self.fields[field].widget.attrs.update({'class':'form-control text-muted'})
#             try:
#                 self.fields[field].widget.attrs.update(
#                 {'maxlength':'%s' % (self.fields[field].max_length,)})
#             except:
#                 continue
#
#         new_fields = OrderedDict()
#         new_fields['country'] = self.fields['country']
#         new_fields['zone'] = self.fields['zone']
#         new_fields['time_zone'] = self.fields['time_zone']
#         new_fields['company'] = self.fields['company']
#         new_fields['name'] = self.fields['name']
#         new_fields['address'] = self.fields['address']
#         new_fields['email'] = self.fields['email']
#         new_fields['image'] = self.fields['image']
#         new_fields['ordered'] = self.fields['ordered']
#         self.fields = new_fields
#
#         self.fields['country'].label = _("Country")
#         self.fields['country'].empty_label = _("Select Country ---")
#         self.fields['country'].label =  mark_safe(
#             "%s <font color=red size=4.5em>*</font>" % self.fields['country'].label) 
#         self.fields['country'].required = True
#
#         self.fields['country'].widget.attrs.update(
#             {'class':'form-control',
#              'onchange':'country_on_changed()'
#              })
#
#         self.fields['zone'].label = _("Country Zone")
#         self.fields['zone'].empty_label = _("Select Country Zone ---")
#         self.fields['zone'].queryset = Zone.objects.filter(id=0)
#         self.fields['zone'].label =  mark_safe(
#             "%s <font color=red size=4.5em>*</font>" % self.fields['zone'].label) 
#
#         self.fields['zone'].widget.attrs.update(
#             {'class':'form-control',
#              'onchange':'zone_on_changed()'
#              })
#         self.fields['zone'].required = True
#
#         self.fields['time_zone'].label = _("Time Zone")
#         self.fields['time_zone'].empty_label = _("Select Time Zone ---")
#         self.fields['time_zone'].queryset = TimeZone.objects.filter(id=0)
#         self.fields['time_zone'].label =  mark_safe(
#             "%s <font color=red size=4.5em>*</font>" % self.fields['time_zone'].label) 
#
#         self.fields['time_zone'].required = True
#
#         self.fields['company'].label = _("Company")
#
#         self.fields['company'].queryset = Company.objects.all().order_by("name")
#         self.fields['company'].label =  mark_safe(
#             "%s <font color=red size=4.5em>*</font>" % self.fields['company'].label) 
#
#         self.fields['name'].label = _("Name")
#         self.fields['name'].label =  mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['name'].label) 
#
#         self.fields['address'].help_text = _("Address, max 1.0 MB.")
#
#         self.fields['image'].help_text = _("Image, max 500 KBytes.")
#         self.fields['image'].widget.attrs.update(
#                         {'accept':"image/*"}
#                         )
#
#         self.fields['ordered'].label =  mark_safe("%s <font color=red size=4.5em>*</font>" % self.fields['ordered'].label) 
#
#         self.fields['company'].empty_label = _("Select Company ---")
#         self.fields['ordered'].widget.attrs.update(
#             {'class':'form-control',
#              'onkeypress':'return isNumberKey(event)',
#             'type':'text'})
#
#     def clean_email(self):
#         data = self.cleaned_data['email']
#         if data:
#             try:
#                 validate_email(data)
#             except:
#                 raise forms.ValidationError(_("Enter a valid email address."))
#
#         return data
#
#     def clean_address(self):
#
#         FILE_SIZE = int(2 * MAX_IMAGE_UPLOAD_SIZE)
#
#         data = self.cleaned_data['address']
#         if data:
#             if len(data.encode('utf-8')) > FILE_SIZE:
#                  raise forms.ValidationError(_('Make sure the Address size is under %s. Now %s') % (
#                      filesizeformat(FILE_SIZE), filesizeformat(len(data.encode('utf-8')))))
#
#         return data
#
#
#     def clean_image(self):
#
#         data = self.cleaned_data['image']
#
#         if data:
#             try:
#                 if int(data.size) > MAX_IMAGE_UPLOAD_SIZE:
#                  raise forms.ValidationError(_('Make sure the attachment file size is under %s. Now %s') % (
#                      filesizeformat(MAX_IMAGE_UPLOAD_SIZE), filesizeformat(data.size)))
#             except:
#                 pass
#
#         return data

    
    
    
    
    
    
