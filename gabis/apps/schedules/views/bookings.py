from __future__ import unicode_literals, absolute_import

import logging
import json

from datetime import date, datetime, timedelta

from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from gabis.core.paginators import SafePaginator
from gabis.apps.users.viewmixins.users import MessageMixin, TaskMixin

from gabis.apps.masters.models.events import (Event, TimeEvent, PICEvent)

log = logging.getLogger(__name__)

class TimeEventZiarahListView(ListView):
    """
        - Level 1
        - Booking with User is self.requests.user
        - Booking with Room with params kwargs pk_datef
    """
    model = TimeEvent
    template_name = "schedules/bookings/events/list.html"
    paginator_class = SafePaginator
    paginate_by = 100
    process = "booking"
    event_filter = "Ziarah Kain Kafan Yesus 2023"
     
    # From 16/07/2023 - 22/07/2023
    date_events = ("16/07/2023","17/07/2023","18/07/2023",
                   "19/07/2023","20/07/2023","21/07/2023",
                   "22/07/2023")
    
    def date2int(self, dstring):
        """format dstring %d/%m/%Y"""
        d = datetime.strptime(dstring, "%d/%m/%Y").date()
        return 10000*d.year + 100*d.month + d.day

    def int2date(self, i):
        year = int(i / 10000)
        month = int((i % 10000) / 100)
        day = int(i % 100)
        return date(year, month, day)
    
    def get_context_data(self, *args, **kwargs):
        
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-0')
        
        # Current parameters filter
        datef = self.request.GET.get('datef','')
        
        # History FIlter
        history_filter = "p0=%s&p1=%s&datef=%s" % (p0, p1, datef)
        history_filter = history_filter.replace('None','').replace('%20','')
        
        # Parameters FIlter
        params_filter = history_filter
        params_filter = params_filter.replace('None','').replace('%20','')
        
        
        # Convert date filter
        if datef in (None,""):
            d = self.date_events[0]
        else:
            d = datetime.strftime(self.int2date(datef),"%d/%m/%Y")
        
        
        datef = dict(
                    dint=self.date2int(d),
                    date=datetime.strptime(d, "%d/%m/%Y").date(),
                    dstr=datetime.strftime(datetime.strptime(d, 
                        "%d/%m/%Y").date(),"%d %h %Y")
                         )
        
        # Set to 08:00 AM
        d = datetime.strptime(d, "%d/%m/%Y") + timedelta(hours=8)
        
        datef.update(ts_dict=dict(
                    year=d.year, 
                    month=d.month-1,
                    day=d.day,
                    hour=d.hour,
                    minute=d.minute,
                    second=d.second
                    )
            )
        
        datef.update(ts_string=datetime.strftime(d, "%Y-%m-%dT%H:%M:%S"))
        
        
        try:
            context = super(TimeEventZiarahListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    datef=datef,
                    object_list=object_list,
                    history_filter=history_filter,
                    params_filter=params_filter,
                    page=page,
                    process=self.process, 
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
                    datef=datef,
                    page_obj=p,
                    object_list=object_list,
                    history_filter=history_filter,
                    params_filter=params_filter,
                    page=page,
                    process=self.process, 
                   ) 
    
    def get_queryset(self):
        
        # Convert date filter
        # datef = self.request.GET.get('datef','')
        # if datef in (None,""):
        #     d = datetime.strptime(self.date_events[0], "%d/%m/%Y").date()
        # else:
        #     d = self.int2date(datef)
        #
        # queryset = self.model.objects.filter(
        #     start_time__year=d.year, start_time__month=d.month, start_time__day=d.day).order_by("created")
            
        queryset = self.model.objects.filter(event__name=self.event_filter).order_by("created")
        
        return queryset