# -*- coding: utf-8 -*-
from __future__ import absolute_import


from django.http import Http404
from django.contrib.auth.mixins import UserPassesTestMixin

# from mongoengine.queryset.visitor import Q as mongo_Q
from django.db.models import Q

from gabis.core.choices import USER_CHOICES


USER_ROLES = ("001","002","003","004","005","006",)

class MessageMixin(UserPassesTestMixin):
    """Message"""
    
    raise_exception = Http404
    
    def get_context_data(self, **kwargs):
        context = super(MessageMixin, self).get_context_data(**kwargs)
        #Please update Message
        from gabis.libs.django_messages.models import Message 
        
        
        user_messages = Message.objects.filter(
            Q(recipient=self.request.user.username,
            read_at__in=(None,""),
            recipient_deleted_at__in=(None,""),
            subject____startswith="NOTIFICATION_")|
            Q(recipient=self.request.user.username,
            read_at__in=(None,""),
            recipient_deleted_at__in=(None,""),
            subject____startswith="MESSAGING_")
            
            ).order_by("-sent_at")
            
        # render message        
        total_messages = len(user_messages)
        
        if user_messages:
            user_messages = user_messages[:3]
        
        # render message        
        context.update(
            dict(
                total_messages=total_messages,
                user_messages=user_messages
                )
            )
        
        
        return context
    
    def test_func(self):
        
        is_authorized = False
        
        if self.request.user.types in USER_ROLES:
            is_authorized = True
       
        return is_authorized
        
       
    
class TaskMixin(UserPassesTestMixin):
    """Task mixin, there are messages for each user"""
    
    raise_exception = Http404
    
    def get_user_trace_ability(self):
        return UserTraceability.objects.filter(
            user=self.request.user, is_active=True
            )
        
    def get_context_data(self, **kwargs):
        context = super(TaskMixin, self).get_context_data(**kwargs)
        
        #Please update Task 
        from gabis.libs.django_messages.models import Message 
        
        user_tasks = Message.objects.filter(
            recipient=self.request.user.username,
            read_at__in=(None,""),
            subject____startswith="TASK_",
            recipient_deleted_at__in=(None,"")).order_by("-sent_at")
        
        total_tasks = len(user_tasks)
        
        if user_tasks:
            user_tasks = user_tasks[:3]
        
        # render message        
        context.update(
            dict(
                total_tasks=total_tasks,
                user_tasks=user_tasks
                )
            )
        
        return context
    
    def test_func(self):
        
        is_authorized = False
        
        if self.request.user.types in USER_ROLES:
            is_authorized = True
       
        return is_authorized