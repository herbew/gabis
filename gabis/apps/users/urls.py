# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import include, path
from gabis.apps.users.views import signin
from gabis.apps.users.views import profiles

app_name = "users"

urlpatterns = [
    # URL pattern for the UserRedirectView
    path("~redirect/",
        view=signin.UserRedirectView.as_view(),
        name="redirect"
    ),
    
    path("update/profile/", 
        profiles.change_profile, 
        name="change_profile"
    ),
]
