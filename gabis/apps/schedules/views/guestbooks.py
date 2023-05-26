# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging
import json
import os 

from itertools import filterfalse, chain

from django.contrib import messages
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView

from braces.views import FormMessagesMixin

from gabis.core.paginators import SafePaginator

from gabis.apps.masters.models.zones import (Keuskupan, Paroki, Wilayah, Lingkungan)
from gabis.apps.masters.models.events import (Event, TimeEvent, PICEvent)
from gabis.apps.schedules.models.bookings import BookingTimeEvent
from gabis.apps.schedules.models.guestbooks import GuestBook
from gabis.apps.schedules.forms.guestbooks import GuestBookForm


log = logging.getLogger(__name__)


class GuestBookListView(LoginRequiredMixin,  
                     ListView):
    """
        Display GuestBook LEVEL 1
    """
    
    model = GuestBook
    template_name = ""
    paginator_class = SafePaginator
    paginate_by = 27
    
    process = "schedules_guest_book" 
    
            
    def get_context_data(self, *args, **kwargs):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2','page-1')
        
        # Active page
        page = self.request.GET.get('page',1)
        
        # History params filter    
        name_university = self.get_faculty().university.name
        faculty_level = self.request.GET.get('faculty_level','')
        faculty_name = self.request.GET.get('faculty_name','')
        
        # Current Filter
        bf_name = self.request.GET.get('bf_name','')
        
        # Filter Notice 
        filter_in = []
            
        if bf_name:
            filter_in.append("%s" % (_("GuestBook's Name")))
            
            
        if filter_in:
            filter_in = "%s %s" % (_("FILTER IN"), ", ".join(filter_in))
        else:
            filter_in = "" 
        
        
        
        # IF p12is "page-1", the template active is Level1
        if p2 != "page-1":
            page = p1
        
        try:
            page = int(page)
        except:
            page = 1
            
        data_filter = dict(
                bf_name=bf_name,
                )
        
        # History FIlter
        history_filter = "p0=%s&p1=%s&name_university=%s&faculty_level=%s&faculty_name=%s" % (
            p0, page, name_university, faculty_level, faculty_name
            )
        history_filter=history_filter.replace('None','')
        
        
        # Param FIlter
        params_filter = "p0=%s&p1=%s&name_university=%s&faculty_level=%s&faculty_name=%s&bf_name=%s" % (
            p0, page, name_university, faculty_level, faculty_name, bf_name)
        
        params_filter = params_filter.replace('None','')
        
    
        try:
            context = super(GuestBookListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    object_list=object_list,
                    form_filter=GuestBookFilterForm(initial=data_filter),
                    history_filter=history_filter.replace('%20',''),
                    params_filter=params_filter.replace('%20',''),
                    page=page,
                    process=self.process, 
                    faculty=self.get_faculty(),
                    filter_in=filter_in
                   ) 
                )
    
            return context
    
        except:
            page = 1
                
            paginator = self.get_paginator(
                self.get_queryset(), self.paginate_by, orphans=self.get_paginate_orphans(),
                allow_empty_first_page=self.get_allow_empty())
            
            try:
                self.object_list = paginator.page(page)
            except PageNotAnInteger:
                self.object_list = paginator.page(1)
            except EmptyPage:
                self.object_list = paginator.page(paginator.num_pages)
                
            object_list = [((index +((page*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(self.object_list,start=0)]
            
            p = dict(paginator=paginator,
                     has_previous=self.object_list.has_previous,
                     number=self.object_list.number,
                     has_next=self.object_list.has_next)
            
            return  dict(
                    page_obj=p,
                    object_list=object_list,
                    form_filter=GuestBookFilterForm(initial=data_filter),
                    history_filter=history_filter.replace('%20',''),
                    params_filter=params_filter.replace('%20',''),
                    page=page,
                    process=self.process, 
                    faculty=self.get_faculty(),
                    filter_in=filter_in
                   ) 
            
    
    def get_queryset(self):
        
        bf_name = self.request.GET.get('bf_name','')
        
        query_set = self.model.objects.filter(
             Q(university=None, level=None, faculty=None, major=None)|
             Q(university=faculty.university, level=None, faculty=None, major=None)|
             Q(university=faculty.university, level=faculty.level, faculty=None, major=None)|
             Q(university=faculty.university, level=faculty.level, faculty=faculty, major=None)
            ).order_by("-university", "-level", "-faculty", "name")
        
        
        if bf_name:
            query_set = query_set.filter(name__icontains=bf_name)
        
        return query_set 
    

class GuestBookCreateView(FormMessagesMixin, 
                       CreateView):
    """
        Create GuestBook at LEVEL 0
    """
    
    model = GuestBook
    form_class = GuestBookForm
    template_name = "schedules/bookings/guestbooks/create.html"
    
    form_invalid_message = _('We are unable to store the registration of guest book, see below for more detail.')
    form_valid_message = _('The registration of guest book has been stored.')
    
    process = "schedules_guest_book" 
    params_filter = ""
    page = 1
    
    def get_success_url(self):
        return reverse_lazy('schedules:time_event_ziarah_list')
    
    def get_time_event(self):
        pk_time_event = self.kwargs.get('pk_time_event','')
        time_event = get_object_or_404(TimeEvent, pk=pk_time_event)
        return time_event
    
    def get_params_url(self):
        # History param filter
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-0')
        
        pk_time_event = self.kwargs.get('pk_time_event','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&pk_time_event=%s" % (
            p0, p1, pk_time_event)
        
        self.params_filter = self.params_filter.replace('None','')
        
        
    def get_context_data(self, *args, **kwargs):
        context = super(GuestBookCreateView, self).get_context_data(*args, **kwargs)
        
        # Get Params URL
        self.get_params_url()
            
        context.update(
            page=self.page,
            process=self.process,
            params_filter=self.params_filter,
            time_event=self.get_time_event()
            )
                
        return context
    
        
    def post(self, request, *args, **kwargs):
        
        # Get Params URL
        self.get_params_url()
        
        self.object = self.model()
        
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        self.messages.error(self.get_form_invalid_message(),
                            fail_silently=True)

        return self.render_to_response(context)

    def form_valid(self, form):
        
        def get_random():
            import random
            r = random.randrange(000000,999999,1)
            
            return "%s" % (r,)
    
        # Searching TypeGuestBook
        time_event = self.get_time_event()
        
        
        # Initial form     
        self.object = form.save(commit=False)
        # Update by user account
        self.object.time_event = time_event
        
        # Get by nik
        try:
            gb = GuestBook.objects.get(nik=self.object.nik)
            pin = gb.pin
        except:
            pin = get_random()
            while GuestBook.objects.filter(pin=pin):
                pin = get_random()
                
        self.object.pin = pin
        self.object.user_updated = self.request.user.username
        
        self.object.save()
        
        # Send out valid message.
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        return HttpResponseRedirect(
                self.get_success_url()
                )