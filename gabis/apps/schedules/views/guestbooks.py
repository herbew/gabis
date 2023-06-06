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
from gabis.apps.schedules.forms.guestbooks import (
        GuestBookForm, 
        GuestBookFilterForm,
        TokenFilterForm,
        GuestBookEventFilterForm)

from _datetime import datetime


log = logging.getLogger(__name__)

SEMINAR_EVENT = "Seminar Kain Kafan Yesus 2023"
ZIARAH_ENVENT = "Ziarah Kain Kafan Yesus 2023"

class GuestBookListView(ListView):
    """
        Display GuestBook LEVEL 1
    """
    
    model = GuestBook
    template_name = ""
    paginator_class = SafePaginator
    paginate_by = 27
    
    process = "schedules_ziarah_guest_book" 
    
            
    def get_context_data(self, *args, **kwargs):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-1')
        
        # Active page
        page = self.request.GET.get('page',1)
        
        # History params filter    
        keuskupan = self.request.GET.get('keuskupan','')
        paroki = self.request.GET.get('paroki','')
        wilayah = self.request.GET.get('wilayah','')
        lingkungan = self.request.GET.get('lingkungan','')
        paid = self.request.GET.get('paid','')
        attended = self.request.GET.get('attended','')
        params = self.request.GET.get('params','')
        
        
        filter_event = self.kwargs.get('filter_event', 1)
        
        if filter_event == 2:
            self.process = "schedules_seminar_guest_book" 
        
        
        # Filter Notice 
        filter_in = []
            
        if keusukupan:
            filter_in.append("%s" % (_("Keuskupan")))
            
        if paroki:
            filter_in.append("%s" % (_("Paroki")))
        
        if wilayah:
            filter_in.append("%s" % (_("Wilayah")))
            
        if lingkungan:
            filter_in.append("%s" % (_("Lingkungan")))
            
        if paid:
            filter_in.append("%s" % (_("Pembayaran")))
        
        if attended:
            filter_in.append("%s" % (_("Kedatangan")))
            
        if params:
            filter_in.append("%s" % (_("Nama/NIK/No Hape dan lainnya")))
            
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
                keuskupan=keuskupan,
                paroki=paroki,
                wilayah=wilayah,
                lingkungan=lingkungan,
                paid=paid,
                attended=attended,
                params=params
                )
        
        # History FIlter
        history_filter = "p0=%s&p1=%s&keuskupan=%s&paroki=%s&wilayah=%s&lingkungan=%s&paid=%s&attended=%s&params=%s" % (
            p0, page, keuskupan, paroki, wilayah,)
        history_filter=history_filter.replace('None','')
        
        
        # Param FIlter
        params_filter = "p0=%s&p1=%s&keuskupan=%s&paroki=%s&wilayah=%s&lingkungan=%s&paid=%s&attended=%s&params=%s" % (
            p0, page, keuskupan, paroki, wilayah,)
        params_filter = params_filter.replace('None','')
        
    
        try:
            context = super(GuestBookListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    object_list=object_list,
                    form_filter=GuestBookEventFilterForm(initial=data_filter),
                    history_filter=history_filter.replace('%20',''),
                    params_filter=params_filter.replace('%20',''),
                    filter_event=filter_event,
                    page=page,
                    process=self.process, 
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
                    form_filter=GuestBookEventFilterForm(initial=data_filter),
                    history_filter=history_filter.replace('%20',''),
                    params_filter=params_filter.replace('%20',''),
                    filter_event=filter_event,
                    page=page,
                    process=self.process, 
                    filter_in=filter_in
                   ) 
            
    
    def get_queryset(self):
        
        # History params filter    
        keuskupan = self.request.GET.get('keuskupan','')
        paroki = self.request.GET.get('paroki','')
        wilayah = self.request.GET.get('wilayah','')
        lingkungan = self.request.GET.get('lingkungan','')
        paid = self.request.GET.get('paid','')
        attended = self.request.GET.get('attended','')
        params = self.request.GET.get('params','')
        
        filter_event = self.kwargs.get('filter_event', 1)
        
        query_set = self.model.objects.filter(time_event__event__id=filter_event)
        
        if keuskupan:
            query_set = query_set.filter(keuskupan=keuskupan)
            
        if paroki:
            query_set = query_set.filter(paroki=paroki)
            
        if wilayah:
            query_set = query_set.filter(wilayah=wilayah)
            
        if lingkungan:
            query_set = query_set.filter(lingkungan=lingkungan)
        
        if paid:
            query_set = query_set.filter(paid=paid)
            
        if attended:
            query_set = query_set.filter(attended=attended)
            
        if params:
            query_set = query_set.filter(
                Q(name__icontains=params)|
                Q(nik__icontains=params)|
                Q(mobile__icontains=params)|
                Q(pin__icontains=params)
                )
            
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
        return "%s?params=%d" % (
            reverse_lazy('schedules:guestbook_detail'), self.object.id)
    
    def get_time_event(self):
        pk_time_event = self.request.GET.get('pk_time_event','')
        time_event = get_object_or_404(TimeEvent, pk=pk_time_event)
        return time_event
    
    def get_params_url(self):
        # History param filter
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-0')
        
        pk_time_event = self.request.GET.get('pk_time_event','')
        
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
            
            r = "%s" % (r,)
            
            if len(r) == 5:
                r = "0%s" % (r)
            elif len(r) == 4:
                r = "00%s" % (r)
            elif len(r) == 3:
                r = "000%s" % (r)
            elif len(r) == 2:
                r = "0000%d" % (r)
            elif len(r) == 1:
                r = "00000%s" % (r)
                
            return r
    
        # Searching TypeGuestBook
        time_event = self.get_time_event()
        
        # Check nik
        if form.cleaned_data['nik']:
            nik = form.cleaned_data['nik']
            
        try:
            self.model.objects.get(nik=nik, time_event__event=time_event.event)
            form.add_error('nik', _('Identity Number have been exists!'))
            context = self.get_context_data(form=form)
            self.messages.error(self.get_form_invalid_message(),
                                fail_silently=True)

            return self.render_to_response(context)
        except:
            pass
        
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
        self.object.user_updated = "System"
        
        self.object.save()
        
        # Send out valid message.
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        return HttpResponseRedirect(
                self.get_success_url()
                )
        
class GuestBookDetailListView(ListView):
    """
        Display Detail GuestBook LEVEL 0
    """
    
    model = GuestBook
    template_name = "schedules/bookings/guestbooks/detail.html"
    paginator_class = SafePaginator
    paginate_by = 1000
    process = "schedules_guest_book" 
    
    guest_book = None

    def get_guest_book(self):
        pk_guest_book = self.request.GET.get('params',0)
        try:
            pk_guest_book = int(pk_guest_book)
        except:
            pk_guest_book = 0

        guest_book = self.model.objects.filter(pk=pk_guest_book)
        if guest_book:
            guest_book = guest_book[0]
            
        return guest_book
        
    def get_context_data(self, *args, **kwargs):
        # Page level 0
        params = self.request.GET.get('params','')
        
        
        # Filter Notice 
        filter_in = []
            
        if params:
            filter_in.append("%s" % (_("Token or NIK or NIS or Mobile Phone Number")))
            
            
        if filter_in:
            filter_in = "%s %s" % (_("FILTER IN"), ", ".join(filter_in))
        else:
            filter_in = "" 
        
            
        data_filter = dict(params=params,)
        
        # History FIlter
        history_filter = "params=%s" % (params,)
        history_filter=history_filter.replace('None','')
        
        
        # Param FIlter
        params_filter = "params=%s" % (params,)
        
        params_filter = params_filter.replace('None','')
        
    
        try:
            context = super(GuestBookDetailListVie, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    object_list=object_list,
                    form_filter=GuestBookFilterForm(initial=data_filter),
                    history_filter=history_filter.replace('%20',''),
                    params_filter=params_filter.replace('%20',''),
                    process=self.process, 
                    guest_book=self.guest_book,
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
                    process=self.process, 
                    guest_book=self.guest_book,
                    filter_in=filter_in
                   ) 
            
    
    def get_queryset(self):
        
        self.guest_book = self.get_guest_book()
        params = self.request.GET.get('params','')
        
        query_set = []
    
        if self.guest_book:
            query_set = self.model.objects.filter(
                 Q(time_event__event__active=True, nik=self.guest_book.nik)|
                 Q(time_event__event__active=True, nik=self.guest_book.pin)
                ).order_by("created")
        elif params:
            query_set = self.model.objects.filter(
                 Q(time_event__event__active=True, nik=params)|
                 Q(time_event__event__active=True, pin=params)).order_by("created")
                
            if query_set:
                self.guest_book = query_set[0]
            
        return query_set 

class AttendGuestView(View):
    model = GuestBook
    process = "schedules_guest_book" 
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        pass
        
    def set_params_url(self, semester):
        pass
        
    def get_object(self):
        pk_guest_book = self.kwargs.get('pk_guest_book',None)
        
        guest_book = get_object_or_404(self.model, pk=pk_guest_book)
        
        return guest_book
    
    def post(self, request, *args, **kwargs):
        
        # Get Params URL
        obj = self.get_object()
        obj.attended = True
        obj.user_updated = request.user.username
        obj.save()
        messages.success(request, _("%r have been attended!." % obj.name))
        
        #return JsonResponse(dict(status=200, url=self.get_success_url()))
        return JsonResponse(self.get_success_url()) 

class SeminarGuestView(View):
    model = GuestBook
    process = "schedules_guest_book" 
    
    def get_success_url(self):
        obj = self.get_object()
        return "%s?params=%d" % (
            reverse_lazy('schedules:guestbook_detail'), obj.id)
    
    def get_params_url(self):
        pass
        
    def set_params_url(self, semester):
        pass
        
    def get_object(self):
        pk_guest_book = self.kwargs.get('pk_guest_book',None)
        
        guest_book = get_object_or_404(self.model, pk=pk_guest_book)
        
        return guest_book
    
    def get(self, request, *args, **kwargs):
        
        # Get Params URL
        obj = self.get_object()
        
        
        seminar_te = TimeEvent.objects.filter(
            event__name=SEMINAR_EVENT,
            event__active=True)
        
        if seminar_te:
            seminar_te = seminar_te[0]
            
            gb_seminar, created = GuestBook.objects.get_or_create(
                time_event=seminar_te, nik=obj.nik,
                defaults=dict(
                    keuskupan=obj.keuskupan,
                    paroki=obj.paroki,
                    wilayah=obj.wilayah,
                    lingkungan=obj.lingkungan,
                    name=obj.name,
                    gender=obj.gender,
                    age=obj.age,
                    email=obj.email,
                    pin=obj.pin)
                )
            
            gb_seminar.user_updated = "System"
            gb_seminar.save()
            messages.success(request, _("%r have been successfully registered!." % gb_seminar.name))
            url =  "%s?params=%d" % (
            reverse_lazy('schedules:guestbook_detail'), gb_seminar.id)
        else:
            messages.error(request, _("No Seminar Event, Please contact to Admin!."))
            url =  "%s?params=%d" % (
            reverse_lazy('schedules:guestbook_detail'), obj.id)
            
        #return JsonResponse(url)   
        return JsonResponse(dict(status=200, url=url))  
    
    def post(self, request, *args, **kwargs):
        
        # Get Params URL
        obj = self.get_object()
        
        
        seminar_te = TimeEvent.objects.filter(
            event__name=SEMINAR_EVENT,
            event__active=True)
        
        if seminar_te:
            seminar_te = seminar_te[0]
            
            gb_seminar, created = GuestBook.objects.get_or_create(
                time_event=seminar_te, nik=obj.nik,
                defaults=dict(
                    keuskupan=obj.keuskupan,
                    paroki=obj.paroki,
                    wilayah=obj.wilayah,
                    lingkungan=obj.lingkungan,
                    name=obj.name,
                    gender=obj.gender,
                    age=obj.age,
                    email=obj.email,
                    pin=obj.pin)
                )
            
            gb_seminar.user_updated = "System"
            gb_seminar.save()
            messages.success(request, _("%r have been successfully registered!." % gb_seminar.name))
            url =  "%s?params=%d" % (
            reverse_lazy('schedules:guestbook_detail'), gb_seminar.id)
        else:
            messages.error(request, _("No Seminar Event, Please contact to Admin!."))
            url =  "%s?params=%d" % (
            reverse_lazy('schedules:guestbook_detail'), obj.id)
            
        return JsonResponse(url)   
        #return JsonResponse(dict(status=200, url=url))  
    
    
class PayGuestView(View):
    model = GuestBook
    process = "schedules_guest_book" 
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        pass
        
    def set_params_url(self, semester):
        pass
        
    def get_object(self):
        pk_guest_book = self.kwargs.get('pk_guest_book',None)
        
        guest_book = get_object_or_404(self.model, pk=pk_guest_book)
        
        return guest_book
    
    def post(self, request, *args, **kwargs):
        
        # Get Params URL
        obj = self.get_object()
        obj.paid = True
        obj.paid_time = datetime.now()
        obj.user_updated = request.user.username
        obj.user_paid = request.user.username
        obj.save()
        messages.success(request, _("%r have been paid!." % obj.name))
        
        #return JsonResponse(dict(status=200, url=self.get_success_url()))
        return JsonResponse(self.get_success_url()) 
    
