from __future__ import unicode_literals, absolute_import

import re, os
import time

from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter(name='year_content')
def year_content(a):
    d = datetime.now().year
    if int(2021) == int(d):
        return ""
    return "- %s" % d

@register.filter(name='message_subject')
def message_subject(a):
    
    a = a.replace("NOTIFICATION_", "")
    a = a.replace("MESSAGING_", "")
    a = a.replace("TASK_", "")
   
    return a

@register.filter(name='message_type')
def message_type(a):
    
    if "NOTIFICATION_" in a:
        return "NOTIFICATION"
    elif "TASK_" in a:
        return "TASK"
    else:
        return "MESSAGING"
    
@register.filter(name='message_subject_popup')
def message_subject_popup(a):
    
    a = a.replace("NOTIFICATION_", "")
    a = a.replace("MESSAGING_", "")
    a = a.replace("TASK_", "")
   
    return "%s.." % a[:10]


@register.filter(name='integer_to_time')
def integer_to_time(a):
    
    return time.strftime('%H:%M:%S', time.gmtime(a))
    
    
