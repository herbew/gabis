# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
import json

from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView

from gabis.apps.masters.models.zones import (Keuskupan, Paroki, Wilayah, Lingkungan)


log = logging.getLogger(__name__)


class AjaxPostParokiView(View):
    
    def post(self, request, *args, **kwargs):
        # Params Filter
        pk_keuskupan = request.POST.get('pk_keuskupan', 0)
        is_filter = request.POST.get('is_filter', False)
        is_required = request.POST.get('is_required', False)
        
        required = is_required
        if is_filter in (True, 'true'):
            required = False
        
        # Return Object Paroki Name
        obj_name = request.POST.get('obj_name', 'paroki')
        obj_id = "id_%s" % (obj_name,)
        
        
        try:
            pk_keuskupan = int(pk_keuskupan)
        except:
            pk_keuskupan = 0
            
        paroki = Paroki.objects.filter(
            keuskupan__id=pk_keuskupan, enabled=True
            ).order_by("keuskupan__name", "name")
        
        
        
        if paroki:
            empty_label = _("Select Paroki ---")
            if is_filter in (True, 'true'):
                empty_label = _("All Paroki ---")
        else:
            empty_label = _("No Paroki !")
             
        obj = forms.ModelChoiceField(
            queryset=paroki,
            empty_label=empty_label,
            required=required,
            widget=forms.Select(attrs={
                'class':'form-control text-muted', 'id':obj_id, 'name':obj_name,
                'onchange':'wilayah_on_change()'
                })
            ).widget
        
        context = {
            "paroki_field" : obj.render(obj_name, '')
        }
    
        context = json.dumps(context, )
    

        return HttpResponse (context, content_type="application/json")
    
class AjaxPostWilayahView(View):
    
    def post(self, request, *args, **kwargs):
        # Params Filter
        pk_paroki = request.POST.get('pk_paroki', 0)
        is_filter = request.POST.get('is_filter', False)
        is_required = request.POST.get('is_required', False)
        
        required = is_required
        if is_filter in (True, 'true'):
            required = False
        
        # Return Object Wilayah Name
        obj_name = request.POST.get('obj_name', 'wilayah')
        obj_id = "id_%s" % (obj_name,)
        
        
        try:
            pk_paroki = int(pk_paroki)
        except:
            pk_paroki = 0
            
        wilayah = Wilayah.objects.filter(
            paroki__id=pk_paroki, enabled=True
            ).order_by("paroki__name", "name")
        
        
        
        if wilayah:
            empty_label = _("Select Wilayah ---")
            if is_filter in (True, 'true'):
                empty_label = _("All Wilayah ---")
        else:
            empty_label = _("No Wilayah !")
             
        obj = forms.ModelChoiceField(
            queryset=wilayah,
            empty_label=empty_label,
            required=required,
            widget=forms.Select(attrs={
                'class':'form-control text-muted', 'id':obj_id, 'name':obj_name,
                'onchange':'lingkungan_on_change()'
                })
            ).widget
        
        context = {
            "wilayah_field" : obj.render(obj_name, '')
        }
    
        context = json.dumps(context, )
    

        return HttpResponse (context, content_type="application/json")  
    
    
class AjaxPostLingkunganView(View):
    
    def post(self, request, *args, **kwargs):
        # Params Filter
        pk_wilayah = request.POST.get('pk_wilayah', 0)
        is_filter = request.POST.get('is_filter', False)
        is_required = request.POST.get('is_required', False)
        
        required = is_required
        if is_filter in (True, 'true'):
            required = False
        
        # Return Object Lingkungan Name
        obj_name = request.POST.get('obj_name', 'lingkungan')
        obj_id = "id_%s" % (obj_name,)
        
        
        try:
            pk_wilayah = int(pk_wilayah)
        except:
            pk_wilayah = 0
            
        lingkungan = Lingkungan.objects.filter(
            wilayah__id=pk_wilayah, enabled=True
            ).order_by("wilayah__name", "name")
        
        
        
        if lingkungan:
            empty_label = _("Select Lingkungan ---")
            if is_filter in (True, 'true'):
                empty_label = _("All Lingkungan ---")
        else:
            empty_label = _("No Lingkungan !")
             
        obj = forms.ModelChoiceField(
            queryset=lingkungan,
            empty_label=empty_label,
            required=required,
            widget=forms.Select(attrs={
                'class':'form-control text-muted', 'id':obj_id, 'name':obj_name,
                })
            ).widget
        
        context = {
            "lingkungan_field" : obj.render(obj_name, '')
        }
    
        context = json.dumps(context, )
    

        return HttpResponse (context, content_type="application/json")  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    