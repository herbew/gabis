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
from gabis.apps.users.models.users import User
from gabis.apps.masters.models.companies import (Company, PICCompany)

from gabis.apps.masters.forms.companies import (
    CompanyForm, UpdatePICCompanyForm, CompanyFilterForm, 
    PICCompanyForm, PICCompanyFilterForm,
    )

log = logging.getLogger(__name__)


class CompanyListView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    ListView):
    """
        Display Company LEVEL 0
    """
    model = Company
    template_name = ""
    paginator_class = SafePaginator
    paginate_by = 27
    process = "company"
        
    def get_context_data(self, *args, **kwargs):
        
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1','page-0')
        
        # Current parameters filter
        cname = self.request.GET.get('cname','')
        
        # Filter Notice 
        filter_in = []
        if cname:
            filter_in.append("%s" % (_("Company Name")))
            
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
            'cname': cname,
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
        params_filter = "%s&cname=%s" % (history_filter, cname)
        params_filter = params_filter.replace('None','').replace('%20','')
        
        try:
            context = super(CompanyListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    object_list=object_list,
                    form_filter=CompanyFilterForm(initial=data_filter),
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
                    form_filter=CompanyFilterForm(initial=data_filter),
                    history_filter=history_filter,
                    params_filter=params_filter,
                    page=page,
                    process=self.process, 
                    filter_in=filter_in
                   ) 
        
        
    def get_queryset(self):
        cname = self.request.GET.get('cname','')
        
        queryset = self.model.objects.all()
            
        if cname:
            queryset = queryset.filter(name__icontains=cname) 
        
        queryset = queryset.order_by('name')
        
        return queryset
    
class CompanyCreateView(LoginRequiredMixin, 
                    FormMessagesMixin,   
                    TaskMixin, MessageMixin, 
                    CreateView):
    """
        Create Company LEVEL 0
    """
    
    model = Company
    form_class = CompanyForm
    template_name = ""
    
    form_invalid_message = _('We are unable to store the Company, see below for more detail.')
    form_valid_message = _('The Company has been stored.')
    
    params_filter = ""
    page = 1
    
    process = "company"
    
    def get_params_url(self):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        cname = self.request.GET.get('cname','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&cname=%s" % (p0, p1, cname)
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, cname):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        cname = cname
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&cname=%s" % (p0, p1, cname)
        self.params_filter = self.params_filter.replace('None','')
    
    def get_context_data(self, *args, **kwargs):
        context = super(CompanyCreateView, self).get_context_data(*args, **kwargs)
        
        self.get_params_url()
        
        types = self.kwargs.get('types','client')
        self.process = types
        
        context.update(
            page=self.request.GET.get('page',1),
            process=self.process,
            params_filter=self.params_filter)
                
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.model()
        is_types = request.POST.get('is_types', '')
        
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form,is_types)
        
        return self.form_invalid(form,is_types)

    def form_invalid(self, form, is_types):
        context = self.get_context_data(form=form)
        
        types = self.kwargs.get('types','client')
        
        if types == 'client':
           self.form_invalid_message = _('We are unable to store the Client, see below for more detail.') 
        
        
        self.messages.error(self.get_form_invalid_message(),
                            fail_silently=True)

        return self.render_to_response(context)

    def form_valid(self, form, is_types):
       
        obj = form.save(commit=False)

        obj.user_updated = self.request.user.username
        obj.save()
        
        self.set_params_url(obj.name)
        
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        return HttpResponseRedirect(self.get_success_url())

class CompanyUpdateView(LoginRequiredMixin, 
                        FormMessagesMixin,  
                        TaskMixin, MessageMixin, 
                        UpdateView):
    
    """
        Update Company LEVEL 0
    """
    
    model = Company
    form_class = CompanyForm
    template_name = ""
    
    form_invalid_message = _('We are unable to update the Company, please scroll down to see the problems.')
    form_valid_message = _('The Company has been updated')
    
    params_filter = ""
    page = 1
    
    process = "company"
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        cname = self.request.GET.get('cname','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&cname=%s" % (p0, p1, cname)
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, cname):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        cname = cname
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&cname=%s" % (p0, p1, cname)
        self.params_filter = self.params_filter.replace('None','')
    
    
    def get_object(self):
        # Only get the User record for the user making the request
        pk_company = self.kwargs.get('pk_company','')
        
        return get_object_or_404(self.model, id=pk_company) 

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        
        self.get_params_url()
        
        context.update(
            object=self.get_object(),
            page=self.request.GET.get('page',1),
            process=self.process,
            params_filter=self.params_filter)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        is_types = request.POST.get('is_types', '')
        
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form,is_types)
        return self.form_invalid(form,is_types)

    def form_invalid(self, form,is_types):
        context = self.get_context_data(form=form)
           
        self.messages.error(self.get_form_invalid_message(),
                            fail_silently=True)

        return self.render_to_response(context)

    def form_valid(self, form,is_types):
        
        old_company = self.get_object()
        
        # Check File Attachment
        if form.cleaned_data['logo']:
            form.instance.logo = form.cleaned_data['logo']
        
        data = self.request.POST
        logo_delete = False
        if 'logo-clear' in data:
            if data['logo-clear'] == 'on':
                logo_delete = True
        
        # Initial form     
        self.object = form.save(commit=False)
        
        url = None
        if logo_delete and old_company.logo:
            
            name = old_company.logo.name
            try:
                cloud_storage = default_storage
                if cloud_storage.exists(name):
                    url = cloud_storage.url(name)
                    cloud_storage.delete(name)
                    
            except:
                pass
            
            try:
                # SOME TIme google any miss about charge
                        
                if old_company.logo.storage.exists(name):
                    url = old_company.logo.storage.url(name)
                    old_company.logo.storage.delete(name)
            except:
                url = old_company.logo.storage.url(name)
            
            self.object.logo = None
            trail_files_user_deleted(
                old_company, url, 
                self.request.user.username)

           
        self.object.user_updated = self.request.user.username
        self.object.save()
        
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        self.set_params_url(cname=self.object.name)
        
        return HttpResponseRedirect(self.get_success_url())
    
class CompanyDeleteView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    View):
    model = Company
    
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
        cname = self.request.GET.get('cname','')
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&cname=%s" % (p0, p1, cname)
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, cname):
        # Page level 0
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
    
        # History Parameters
        
        # Current Parameters
        cname = cname
        
        try:
            self.page = int(p0)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&cname=%s" % (p0, p1, cname)
        self.params_filter = self.params_filter.replace('None','')
    
    def get_object(self):
        # Only get the User record for the user making the request
        pk_company = self.kwargs.get('pk_company','')
        
        return get_object_or_404(self.model, id=pk_company) 
    
    def post(self, request, *args, **kwargs):
        # Get Params URL
        self.get_params_url()
        
        obj = self.get_object()
        
        company_name =  obj.name
        
        obj.delete()
        
        first_message = _("The record")
        end_message = _("has successfully deleted it!")
        
        self.set_params_url(cname="")
        
        messages.success(request, "%s %s %s" % (first_message, company_name, end_message))
        
        return JsonResponse(self.get_success_url())
        
    
class PICCompanyListView(LoginRequiredMixin, 
                    TaskMixin, MessageMixin, 
                    ListView):
    model = PICCompany
    template_name = ""
    paginator_class = SafePaginator
    paginate_by = "27"
    process = "company"
     
    def get_company(self):
        # Only get the User record for the user making the request
        pk_company = self.kwargs.get('pk_company','')
        
        company = get_object_or_404(Company, pk=pk_company)
        return company
    
    def get_context_data(self, *args, **kwargs):
        
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2','page-1')
        
        # History parameters filter
        cname = self.request.GET.get('cname','')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        pic_name = self.request.GET.get('pic_name','')
        
        # Filter Notice 
        filter_in = []
        if company:
            filter_in.append("%s" % (_("Company")))
        
        if pic_name:
            filter_in.append("%s" % (_("PIC Name")))
            
        if filter_in:
            filter_in = "%s %s" % (_("FILTER IN"), ", ".join(filter_in))
        else:
            filter_in = "" 
        
        
        # IF p2 is "page-1", the template active is Level0
        if p2 != "page-1":
            page = p1
        
        try:
            page = int(page)
        except:
            page = 1
            
        data_filter = {
            'company': company,
            'pic_name': pic_name
            }
        
        # Set number records
        try:
            page = int(self.request.GET.get('page',1))
        except:
            page = 1
            
        
        # History FIlter
        history_filter = "p0=%s&p1=%s&p2=%s&cname=%s" % (p0, p1, p2, cname)
        history_filter = history_filter.replace('None','').replace('%20','')
        
        # Parameters FIlter
        params_filter = "%s&company=%s&pic_name=%s" % (history_filter, company, pic_name)
        params_filter = params_filter.replace('None','').replace('%20','')
        
        try:
            context = super(PICCompanyListView, self).get_context_data(*args, **kwargs)
            object_list = [((index +((int(page)*int(self.paginate_by))
                -int(self.paginate_by)))+1,q) for index, q in 
                enumerate(context["object_list"],start=0)]
            
            context.update(
                dict(
                    company=self.get_company(),
                    object_list=object_list,
                    form_filter=PICCompanyFilterForm(initial=data_filter),
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
                    company=self.get_company(),
                    page_obj=p,
                    object_list=object_list,
                    form_filter=PICCompanyFilterForm(initial=data_filter),
                    history_filter=history_filter,
                    params_filter=params_filter,
                    page=page,
                    process=self.process, 
                    filter_in=filter_in
                   ) 
            
        context = super(PICCompanyListView, self).get_context_data(*args, **kwargs)
        
        
    def get_queryset(self):
        company = self.request.GET.get('company','')
        pic_name = self.request.GET.get('pic_name','')
        
        queryset = self.model.objects.all()
        
        if company:
            queryset = queryset.filter(company__id=company) 
            
        if pic_name:
            queryset = queryset.filter(pic__name__icontains=pic_name) 
         
        
        queryset = queryset.order_by('pic__name')
        
        return queryset
    
class PICCompanyCreateView(LoginRequiredMixin, FormMessagesMixin,
                           TaskMixin, MessageMixin, 
                           CreateView):
    model = PICCompany
    form_class = PICCompanyForm
    template_name = ""
     
    form_invalid_message = _('We are unable to store the PIC Company, see below for more detail.')
    form_valid_message = _('The PIC Company has been stored.')
    
    params_filter = ""
    page = 1
    
    process = "company"
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
        
        # History parameters filter
        cname = self.request.GET.get('cname','')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        pic_name = self.request.GET.get('pic_name','')
        
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&cname=%s&company=%s&pic_company=%s" % (
            p0, p1, p2, cname, company, pic_name)
        
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, name):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
        
        # History parameters filter
        cname = self.request.GET.get('cname','')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        pic_name = name
        
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&cname=%s&company=%s&pic_company=%s" % (
            p0, p1, p2, cname, company, pic_name)
        
        self.params_filter = self.params_filter.replace('None','')
    
    def get_company(self):
        # Only get the User record for the user making the request
        pk_company = self.kwargs.get('pk_company','')
        company = get_object_or_404(Company,pk=pk_company)
        
        return company
          
    def get_context_data(self, *args, **kwargs):
        context = super(PICCompanyCreateView, self).get_context_data(*args, **kwargs)
        
        self.get_params_url()
        
        context.update(
            company = self.get_company(),
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
        
        # Get Post data from form
        data = self.request.POST
        username = data['username']
        name = data['name']
        email = data['email']
        password = data['password1']
        gender = data['gender']
        
        user, created = User.objects.get_or_create(username=username)
        user.name = name
        user.email = email
        user.gender = gender
        user.set_password(password)
        user.user_updated = self.request.user.username
        user.save()
        
        obj = form.save(commit=False)
        obj.pic = user
        obj.company = self.get_company()
        obj.user_updated = self.request.user.username
        obj.save()
        
        self.set_params_url(name=obj.pic.name)
        
        # Send out valid message.
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        
        return HttpResponseRedirect(self.get_success_url())
    
class PICCompanyUpdateView(LoginRequiredMixin, FormMessagesMixin,  
                           TaskMixin, MessageMixin, 
                           UpdateView):
    model = PICCompany
    form_class = UpdatePICCompanyForm
    template_name = ""
     
    form_invalid_message = _('We are unable to update the PIC Company, please scroll down to see the problems.')
    form_valid_message = _('The PIC Company has been updated')
    
    params_filter = ""
    page = 1
    
    process = "company"
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
        
        # History parameters filter
        cname = self.request.GET.get('cname','')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        pic_name = self.request.GET.get('pic_name','')
        
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&cname=%s&company=%s&pic_company=%s" % (
            p0, p1, p2, cname, company, pic_name)
        
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, name):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
        
        # History parameters filter
        cname = self.request.GET.get('cname','')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        pic_name = name
        
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&cname=%s&company=%s&pic_company=%s" % (
            p0, p1, p2, cname, company, pic_name)
        
        self.params_filter = self.params_filter.replace('None','')
        
    def get_object(self):
        # Only get the User record for the user making the request
        pk_pic_company = self.kwargs.get('pk_pic_company','')
        pic_company = get_object_or_404(self.model, pk=pk_pic_company)
        
        return pic_company
        
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        
        obj = self.get_object()
        
        return dict(
                name=obj.pic.name,
                gender=obj.pic.gender
            )
        
    def get_context_data(self, **kwargs):
        context = super(PICCompanyUpdateView, self).get_context_data(**kwargs)
        
        self.get_params_url()
        
        context.update(
            company = self.get_object().company,
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
        
        # Get Post data from form
        data = self.request.POST
        name = data['name']
        email = data['email']
        gender = data['gender']
        
        user = User.objects.get(pk=self.object.pic.pk)
        user.name = name
        user.email = email
        user.gender = gender
        user.user_updated = self.request.user.username
        user.save()
        
        obj = form.save(commit=False)
        obj.user_updated = self.request.user.username
        obj.save()
        
        # Send out valid message.
        self.messages.success(self.get_form_valid_message(),
                              fail_silently=True)
        self.set_params_url(name=obj.pic.name)
        
        return HttpResponseRedirect(self.get_success_url())

class PICCompanyDeleteView(LoginRequiredMixin,  
                           TaskMixin, MessageMixin, 
                           View):
    model = PICCompany
    company_pk = None
    
    def get_success_url(self):
        pass
    
    def get_params_url(self):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
        
        # History parameters filter
        cname = self.request.GET.get('cname','')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        pic_name = self.request.GET.get('pic_name','')
        
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&cname=%s&company=%s&pic_company=%s" % (
            p0, p1, p2, cname, company, pic_name)
        
        self.params_filter = self.params_filter.replace('None','')
    
    def set_params_url(self, name):
        # Page level 1
        p0 = self.request.GET.get('p0',1)
        p1 = self.request.GET.get('p1',1)
        p2 = self.request.GET.get('p2',1)
        
        # History parameters filter
        cname = self.request.GET.get('cname','')
        
        # Current parameters filter
        company = self.request.GET.get('company','')
        pic_name = name
        
        
        try:
            self.page = int(p1)
        except:
            self.page = 1
        
        self.params_filter = "p0=%s&p1=%s&p2=%s&cname=%s&company=%s&pic_company=%s" % (
            p0, p1, p2, cname, company, pic_name)
        
        self.params_filter = self.params_filter.replace('None','')
        
    def post(self, request, *args, **kwargs):
        pk_pic_company = self.kwargs.get('pk_pic_company','')
        
        first_message = _("The record")
        end_message = _("has successfully deleted it!")
        
        self.get_params_url()
        
        try:
            obj = self.model.objects.get(pk=pk_pic_company)
            self.company_pk = obj.company.pk
            obj_str = "%s" % (obj.pic.name)
            
            obj.delete()
            
            messages.success(request, "%s %s %s" % (obj_str, first_message, end_message))
        except:
            messages.warning(request, _("The process was failed"))
        
        self.set_params_url(name="")
        
        return JsonResponse(self.get_success_url())
  
    
    
    
