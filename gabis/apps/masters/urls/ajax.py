from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.masters.views import ajax

urlpatterns = [
    
    path("ajax/types/company/change/", 
        view=ajax.AjaxTypesCompanyChangeView.as_view(),
        name="ajax_types_company_change"),
    
    
    ]