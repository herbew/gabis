
from __future__ import absolute_import, unicode_literals
import logging

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from allauth.account.models import EmailAddress

from gabis.apps.users.models.users import User
from gabis.apps.users.forms import UserUpdateForm

log = logging.getLogger(__name__)

@login_required
def change_profile(request):
    
    user = User.objects.get(id=request.user.pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():

            obj = form.save(commit=False)
            obj.save()
            
            user.user_updated = request.user.username
            user.save()
        
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('users:change_profile')
        
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        obj = dict(
                name=user.name, 
                gender=user.gender, 
                mobile=user.mobile,
                address=user.address,
                birth_city=user.birth_city,
                birth_date=user.birth_date,
            )
        
        form = UserUpdateForm(initial=obj)
        
    return render(request, 'users/profile_change.html', {
        'form': form
    })



  
