from __future__ import unicode_literals, absolute_import

import logging
import json

from datetime import datetime, timedelta

from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from gabis.core.paginators import SafePaginator
from gabis.apps.users.viewmixins.users import MessageMixin, TaskMixin

from gabis.apps.schedules.models.biostars import BiostarRoom
from gabis.apps.schedules.models.bookings import BookingRoom
from gabis.apps.schedules.models.users import UserBookingRoom
from gabis.apps.schedules.forms.bookings import UserBookingRoomFilterForm


log = logging.getLogger(__name__)


class UserBookingRoomListView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    ListView):
    """
        Display UserBookingRoom LEVEL 0
    """
    model = UserBookingRoom
    template_name = ""
    paginator_class = SafePaginator
    paginate_by = 27
    process = "booking"
        
    def get_context_data(self, *args, **kwargs):
        
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-0')
        
        # Current parameters filter
        room = self.request.GET.get('room','')
        users = self.request.GET.get('users','')
        
        # Filter Notice 
        filter_in = []
        if room:
            filter_in.append("%s" % (_("Buliding or Room")))
            
        if users:
            filter_in.append("%s" % (_("User")))
            
        if filter_in:
            filter_in = "%s %s" % (_("FILTER IN"), ", ".join(filter_in))
        else:
            filter_in = "" 
        
        
        # IF p1 is "page-0", the template active is Level0
        if p1 != "page-0":
            page = p0
        
        try:
            page = int(page)
        except:
            page = 1
            
        data_filter = {
            'room': room,
            'users': users,
            }
        
        # Set number records
        try:
            page = int(self.request.GET.get('page',1))
        except:
            page = 1
            
        
        # History FIlter
        history_filter = "p0=%s&p1=%s" % (p0,p1)
        history_filter = history_filter.replace('None','').replace('%20','')
        
        # Parameters FIlter
        params_filter = "%s&room=%s&users=%s" % (history_filter, room, users)
        params_filter = params_filter.replace('None','').replace('%20','')
        
        try:
            context = super(UserBookingRoomListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    object_list=object_list,
                    form_filter=UserBookingRoomFilterForm(initial=data_filter),
                    history_filter=history_filter,
                    params_filter=params_filter,
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
                    form_filter=UserBookingRoomFilterForm(initial=data_filter),
                    history_filter=history_filter,
                    params_filter=params_filter,
                    page=page,
                    process=self.process, 
                    filter_in=filter_in
                   ) 
        
        
    def get_queryset(self):
        room = self.request.GET.get('room','')
        users = self.request.GET.get('users','')
        
        queryset = self.model.objects.all().order_by("-created")
        
        if room:
           queryset = queryset.filter(
               Q(biostar_room__room__name__icontains=room)|
               Q(biostar_room__room__building__name__icontains=room)
               )
           
        if users:
            queryset = queryset.filter(
                Q(users__name__icontains=users)|
                Q(users__username__icontains=users)|
                Q(users__email__icontains=users)) 
        
        return queryset
    

class BookingRoomListView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    ListView):
    """
        - Level 1
        - Booking with User is self.requests.user
        - Booking with Room with params kwargs pk_room
    """
    model = BookingRoom
    template_name = ""
    paginator_class = SafePaginator
    paginate_by = 27
    process = "booking"
    
    def get_biostar_room(self):
        pk_biostar_room = self.kwargs.get('pk_biostar_room','')
        
        return get_object_or_404(BiostarRoom, pk=pk_biostar_room) 
    
    def get_context_data(self, *args, **kwargs):
        
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-0')
        
        # Current parameters filter
        room = self.request.GET.get('room','')
        users = self.request.GET.get('users','')
        
        # History FIlter
        history_filter = "p0=%s&p1=%s&room=%s&users=%s" % (p0, p1, room, users)
        history_filter = history_filter.replace('None','').replace('%20','')
        
        # Parameters FIlter
        params_filter = history_filter
        params_filter = params_filter.replace('None','').replace('%20','')
        
        biostar_room = self.get_biostar_room()
        ts_biostar_room = datetime.utcnow()
        delta_hour = biostar_room.room.gmt_offset_hour
        
        if delta_hour >= 0:
            ts_biostar_room = ts_biostar_room + timedelta(hours=abs(delta_hour))
        else:
            ts_biostar_room = ts_biostar_room - timedelta(hours=abs(delta_hour))
        
        
        ts_dict = dict(
            year=ts_biostar_room.year, 
            month=ts_biostar_room.month-1,
            day=ts_biostar_room.day,
            hour=ts_biostar_room.hour,
            minute=ts_biostar_room.minute,
            second=ts_biostar_room.second
            )
        
        ts_biostar_room_string = datetime.strftime(ts_biostar_room, "%Y-%m-%dT%H:%M:%S")
        
        try:
            context = super(UserBookingRoomListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    biostar_room=biostar_room,
                    ts_biostar_room=ts_biostar_room,
                    ts_biostar_room_string=ts_biostar_room_string,
                    ts_dict=ts_dict,
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
                    biostar_room=biostar_room,
                    ts_biostar_room=ts_biostar_room,
                    ts_biostar_room_string=ts_biostar_room_string,
                    ts_dict=ts_dict,
                    page_obj=p,
                    object_list=object_list,
                    history_filter=history_filter,
                    params_filter=params_filter,
                    page=page,
                    process=self.process, 
                   ) 
    
    def get_queryset(self):
        
        pk_biostar_room = self.kwargs.get('pk_biostar_room','')
        
        queryset = self.model.objects.filter(
            biostar_room__pk=pk_biostar_room).order_by("-created")
        
        return queryset