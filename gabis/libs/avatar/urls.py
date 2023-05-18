# try:
#     from django.urls import include, path
# except ImportError:
#     # Django < 1.4
#     from django.conf.urls.defaults import url
    
from django.urls import path

from . import views

app_name = "avatar"

urlpatterns = [
    path("add", views.add, name='avatar_add'),
    path("change", views.change, name='avatar_change'),
    path("delete", views.delete, name='avatar_delete')
]
