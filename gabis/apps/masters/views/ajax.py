# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
import json

from django import forms
from django.http import HttpResponse
from django.views.generic import View
from braces.views import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _

from gabis.apps.masters.models.companies import Company

log = logging.getLogger(__name__)

class AjaxTypesCompanyChangeView(LoginRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        
        types = request.POST.get('types', 'client')
        
        is_filter = request.POST.get('is_filter', False)
        is_required = request.POST.get('is_required', False)
        
        required = is_required
        if is_filter in (True, 'true'):
            required = False
        
        # Return Object Faculty Name
        obj_name = request.POST.get('obj_name', 'company')
        obj_id = "id_%s" % (obj_name,)
        
        if types == 'client':
            company = Company.objects.filter(types__in=('01',1,'03',3))
        else:
            company = Company.objects.filter(types__in=('02',2,'03',3))
            
        if company:
            empty_label = _("Select Company ---")
            if is_filter in (True, 'true'):
                empty_label = _("All Companies ---")
        else:
            empty_label = _("No Company !")
        
        obj = forms.ModelChoiceField(
                queryset=company,
                empty_label=empty_label,
                required=required,
                widget=forms.Select(attrs={
                'class':'form-control text-muted', 'id':obj_id, 'name':obj_name,
                })
            ).widget
        
        context = {
            "company_field" : obj.render('company', '')
        }
    
        context = json.dumps(context, )

        return HttpResponse (context, content_type="application/json")