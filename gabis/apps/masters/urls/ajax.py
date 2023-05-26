from __future__ import absolute_import, unicode_literals

from django.urls import include, path

from gabis.apps.masters.views import zones

urlpatterns = [
    
    path("ajax/post/paroki/change/", 
        view=zones.AjaxPostParokiView.as_view(),
        name="ajax_post_paroki_change"),
    
    path("ajax/post/wilayah/change/", 
        view=zones.AjaxPostWilayahView.as_view(),
        name="ajax_post_wilayah_change"),
    
    path("ajax/post/lingkungan/change/", 
        view=zones.AjaxPostLingkunganView.as_view(),
        name="ajax_post_lingkungan_change"),
    
    
    ]