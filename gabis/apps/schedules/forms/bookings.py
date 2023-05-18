from __future__ import unicode_literals, absolute_import

import logging

from django import forms
from django.utils.safestring import mark_safe
from django.forms.widgets import Select, TextInput, CheckboxInput
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)

class UserBookingRoomFilterForm(forms.Form):
    room = forms.CharField(
        label=_("Building or Room Name"),
        widget = TextInput(attrs={'class':'form-control'}),
        required=False
    )
    
    users = forms.CharField(
        label=_("Name, Username, or Email of User"),
        widget = TextInput(attrs={'class':'form-control'}),
        required=False
    )