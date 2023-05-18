from __future__ import unicode_literals, absolute_import

import logging
import json

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import  FormMessagesMixin

from gabis.core.paginators import SafePaginator
from gabis.apps.users.viewmixins.users import MessageMixin, TaskMixin

from gabis.apps.trails.views.utils import (
    trail_files_user_deleted, trail_summernote_user_deleted
    )

from gabis.apps.localized.models.zones import (
    Country, Zone, TimeZone
    )

from gabis.apps.masters.models.buildings import (Building, Room)

from gabis.apps.masters.forms.buildings import (
    BuildingForm, BuildingFilterForm, 
    RoomForm, RoomFilterForm,
    )

log = logging.getLogger(__name__)


class BuildingListView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    ListView):
    """
        Display Building LEVEL 0
    """
    model = Building
    template_name = ""
    paginator_class = SafePaginator
    paginate_by = 27
    process = "room"
        
    def get_context_data(self, *args, **kwargs):
        
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-0')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        # Filter Notice 
        filter_in = []
        if company:
            filter_in.append("%s" % (_("Company")))
            
        if building:
            filter_in.append("%s" % (_("Building Name")))
            
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
            'company': company,
            'building': building,
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
        params_filter = "%s&company=%s&building=%s" % (history_filter, company, building)
        params_filter = params_filter.replace('None','').replace('%20','')
        
        try:
            context = super(BuildingListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    object_list=object_list,
                    form_filter=BuildingFilterForm(initial=data_filter),
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
                    form_filter=BuildingFilterForm(initial=data_filter),
                    history_filter=history_filter,
                    params_filter=params_filter,
                    page=page,
                    process=self.process, 
                    filter_in=filter_in
                   ) 
        
        
    def get_queryset(self):
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        queryset = self.model.objects.all().order_by("company","ordered")
        
        if company:
           queryset = queryset.filter(company__id=company)
           
        if building:
            queryset = queryset.filter(name__icontains=building) 
        
        return queryset
    
class BuildingCreateView(LoginRequiredMixin, 
                    FormMessagesMixin,   
                    TaskMixin, MessageMixin, 
                    CreateView):
    """
        Create Building LEVEL 0
    """
    
    model = Building
    form_class = BuildingForm
    template_name = ""
    
    form_invalid_message = _('We are unable to store the Building, see below for more detail.')
    form_valid_message = _('The Building has been stored.')
    
    params_filter = ""
    page = 1
    
    process = "room"
    
    def get_params_url(self):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, building):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = building
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    def get_context_data(self, *args, **kwargs):
        context = super(BuildingCreateView, self).get_context_data(*args, **kwargs)
        
        self.get_params_url()
        
        context.update(
            page=self.request.GET.get('page',1),
            process=self.process,
            params_filter=self.params_filter)
                
        return context
        
    def post(self, request, *args, **kwargs):
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
       
        obj = form.save(commit=False)

        # Send out valid message.
        obj.user_updated = self.request.user.username
        obj.save()
        
        self.set_params_url(building=obj.name)
        
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        return HttpResponseRedirect(self.get_success_url())

class BuildingUpdateView(LoginRequiredMixin, 
                        FormMessagesMixin,  
                        TaskMixin, MessageMixin, 
                        UpdateView):
    
    """
        Update Building LEVEL 0
    """
    
    model = Building
    form_class = BuildingForm
    template_name = ""
    
    form_invalid_message = _('We are unable to update the Building, please scroll down to see the problems.')
    form_valid_message = _('The Building has been updated')
    
    params_filter = ""
    page = 1
    
    process = "room"
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, building):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = building
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    
    def get_object(self):
        # Only get the User record for the user making the request
        pk = self.kwargs.get('pk_building','')
        
        return get_object_or_404(self.model, id=pk) 

    def get_context_data(self, **kwargs):
        context = super(BuildingUpdateView, self).get_context_data(**kwargs)
        
        self.get_params_url()
        
        context.update(
            object=self.get_object(),
            page=self.request.GET.get('page',1),
            process=self.process,
            params_filter=self.params_filter)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
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
        
        old_building = self.get_object()
        
        # Check File Attachment
        if form.cleaned_data['image']:
            form.instance.image = form.cleaned_data['image']
        
        data = self.request.POST
        image_delete = False
        if 'image-clear' in data:
            if data['image-clear'] == 'on':
                image_delete = True
        
        # Initial form     
        self.object = form.save(commit=False)
        
        url = None
        if image_delete and old_building.image:
            
            name = old_building.image.name
            try:
                cloud_storage = default_storage
                if cloud_storage.exists(name):
                    url = cloud_storage.url(name)
                    cloud_storage.delete(name)
                    
            except:
                pass
            
            try:
                # SOME TIme google any miss about charge
                        
                if old_building.image.storage.exists(name):
                    url = old_building.image.storage.url(name)
                    old_building.image.storage.delete(name)
            except:
                url = old_building.image.storage.url(name)
            
            self.object.image = None
            trail_files_user_deleted(
                old_building, url, 
                self.request.user.username)

        self.object.user_updated = self.request.user.username
        self.object.save()
        
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        self.set_params_url(building=self.object.name)
        
        return HttpResponseRedirect(self.get_success_url())
    
class BuildingUpdateTimeZoneView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    View):
    model = Building
    
    params_filter = ""
    page = 1
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, building):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = building
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    def get_object(self):
        # Only get the User record for the user making the request
        pk_building = self.kwargs.get('pk_building','')
        
        return get_object_or_404(self.model, id=pk_building) 
    
    def post(self, request, *args, **kwargs):
        # Get Params URL
        self.get_params_url()
        
        # Get Paramenter POST
        pk_country = request.POST.get('pk_country', 0)
        pk_zone = request.POST.get('pk_zone', 0)
        pk_time_zone = request.POST.get('pk_time_zone', 0)
        
        try:
            country = Country.objects.get(pk=pk_country)
        except:
            messages.error(request, _("The data Country not exists!!"))
            return JsonResponse(self.get_success_url())
        
        try:
            zone = Zone.objects.get(pk=pk_zone)
        except:
            messages.error(request, _("The data Country Zone not exists!!"))
            return JsonResponse(self.get_success_url())
        
        try:
            time_zone = TimeZone.objects.get(pk=pk_time_zone)
        except:
            messages.error(request, _("The data Time Zone not exists!!"))
            return JsonResponse(self.get_success_url())
        
        
        obj = self.get_object()
        
        obj.country = country
        obj.zone = zone
        obj.time_zone = time_zone
        obj.user_updated = self.request.user.username
        
        obj.save()
        
        
        first_message = _("The time zone")
        end_message = _("has successfully update it!")
        
        self.set_params_url(building="")
        
        messages.success(request, "%s %s %s" % (first_message, obj.name, end_message))
        
        return JsonResponse(self.get_success_url())

class BuildingDeleteView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    View):
    model = Building
    
    params_filter = ""
    page = 1
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, building):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        company = self.request.GET.get('company','')
        building = building
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&company=%s&building=%s" % (p0, p1, company, building)
        self.params_filter = self.params_filter.replace('None','')
    
    def get_object(self):
        # Only get the User record for the user making the request
        pk_building = self.kwargs.get('pk_building','')
        
        return get_object_or_404(self.model, id=pk_building) 
    
    def post(self, request, *args, **kwargs):
        # Get Params URL
        self.get_params_url()
        
        obj = self.get_object()
        
        building_name =  obj.name
        
        obj.delete()
        
        first_message = _("The record")
        end_message = _("has successfully deleted it!")
        
        self.set_params_url(building="")
        
        messages.success(request, "%s %s %s" % (first_message, building_name, end_message))
        
        return JsonResponse(self.get_success_url())
        

class RoomCreateView(LoginRequiredMixin, FormMessagesMixin,
                           TaskMixin, MessageMixin, 
                           CreateView):
    model = Room
    form_class = RoomForm
    
    template_name = ""
    
    form_invalid_message = _('We are unable to store the Room, see below for more detail.')
    form_valid_message = _('The Room has been stored.')
    
    params_filter = ""
    page = 1
    
    process = "room"
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
    
        
        # History parameters filter
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        # Current parameters filter
        room = self.request.GET.get('room','')
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&company=%s&building=%s&room=%s" % (
            p0, p1, p2, company, building, room)
        
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, building, name):
         # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
    
        
        # History parameters filter
        company = self.request.GET.get('company','')
        building = building
        
        # Current parameters filter
        room = name
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&company=%s&building=%s&room=%s" % (
            p0, p1, p2, company, building, room)
        
        self.params_filter = self.params_filter.replace('None','')
        
    
    def get_building(self):
        # Only get the User record for the user making the request
        pk_building = self.kwargs.get('pk_building','')
        
        building = get_object_or_404(Building, pk=pk_building)
        
        return building
          
    def get_context_data(self, *args, **kwargs):
        context = super(RoomCreateView, self).get_context_data(*args, **kwargs)
        
        self.get_params_url()
        
        context.update(
            building=self.get_building(),
            page=self.request.GET.get('page',1),
            process=self.process,
            param_filter=self.params_filter
            )
                
        return context
    
    def post(self, request, *args, **kwargs):
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
        obj = form.save(commit=False)
        building = self.get_building()
        name = form.cleaned_data['name']
        
        room = Room.objects.filter(building=building, name=name)
        
        if room:
            # Send out valid message.
            messages.error(self.request, _("The name of Room already exists!"))
        else:
            obj.building = building
            obj.user_updated = self.request.user.username
            obj.save()
    
            # Send out valid message.
            self.messages.success(self.get_form_valid_message(),
                                  fail_silently=True)
            
        
        self.set_params_url(building=building.name, name=name)
        
        return HttpResponseRedirect(self.get_success_url())
    
        
class RoomUpdateView(LoginRequiredMixin, FormMessagesMixin,  
                           TaskMixin, MessageMixin, 
                           UpdateView):
    model = Room
    form_class = RoomForm
    template_name = ""
    
    form_invalid_message = _('We are unable to update the Room, please scroll down to see the problems.')
    form_valid_message = _('The Room has been updated')
    
    params_filter = ""
    page = 1
    
    
    process = "room"
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
    
        
        # History parameters filter
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        # Current parameters filter
        room = self.request.GET.get('room','')
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&company=%s&building=%s&room=%s" % (
            p0, p1, p2, company, building, room)
        
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, building, name):
         # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
    
        
        # History parameters filter
        company = self.request.GET.get('company','')
        building = building
        
        # Current parameters filter
        room = name
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&company=%s&building=%s&room=%s" % (
            p0, p1, p2, company, building, room)
        
        self.params_filter = self.params_filter.replace('None','')
        
    def get_object(self):
        # Only get the User record for the user making the request
        
        pk_room = self.kwargs.get('pk_room','')
        
        return get_object_or_404(self.model, pk=pk_room )

    def get_context_data(self, **kwargs):
        context = super(RoomUpdateView, self).get_context_data(**kwargs)
        
        self.get_params_url()
        
        context.update(
            building = self.get_object().building,
            page=self.request.GET.get('page',1),
            process=self.process,
            param_filter=self.params_filter
            )
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
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
        obj = form.save(commit=False)
        obj.user_updated = self.request.user.username
        obj.save()
        
        building = obj.building
        
        # Send out valid message.
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        self.set_params_url(building=building.name, name=obj.name)
        
        return HttpResponseRedirect(self.get_success_url())


class RoomDeleteView(LoginRequiredMixin,  
                           TaskMixin, MessageMixin, 
                           View):
    model = Room
    pk_building = None
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
    
        
        # History parameters filter
        company = self.request.GET.get('company','')
        building = self.request.GET.get('building','')
        
        # Current parameters filter
        room = self.request.GET.get('room','')
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&company=%s&building=%s&room=%s" % (
            p0, p1, p2, company, building, room)
        
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, building, name):
         # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
    
        
        # History parameters filter
        company = self.request.GET.get('company','')
        building = building
        
        # Current parameters filter
        room = name
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&company=%s&building=%s&room=%s" % (
            p0, p1, p2, company, building, room)
        
        self.params_filter = self.params_filter.replace('None','')
        
    def get_object(self):
        # Only get the User record for the user making the request
        
        pk_room = self.kwargs.get('pk_room','')
        
        return get_object_or_404(self.model, pk=pk_room )
        
    def post(self, request, *args, **kwargs):
        pk_room = self.kwargs.get('pk_room','')
        
        first_message = _("The record")
        end_message = _("has successfully deleted it!")
        
        
        obj = self.get_object()
        
        building = obj.building
        
        self.pk_building = building.pk
        obj_str = "%s" % (obj.name)
        obj.delete()
        
        messages.success(request, "%s %s %s" % (
            first_message, obj_str,  end_message))
        
        
        self.set_params_url(building=building.name, name="")
        
        return JsonResponse(self.get_success_url())
