from django.urls import include, path
from django.views.generic import RedirectView

from gabis.libs.django_messages.views import *

app_name="django_messages"

urlpatterns = [
    path("redirect/", RedirectView.as_view(permanent=True, url='inbox/'), name='messages_redirect'),
    path("inbox/", inbox, name='messages_inbox'),
    path("outbox/", outbox, name='messages_outbox'),
    path("compose/", compose, name='messages_compose'),
    path("compose/<str:recipient>/", compose, name='messages_compose_to'),
    path("reply/<str:message_id>", reply, name='messages_reply'),
    path("view/<str:message_id>", view, name='messages_detail'),
    path("delete/<str:message_id>", delete, name='messages_delete'),
    path("undelete/<str:message_id>", undelete, name='messages_undelete'),
    path("trash/", trash, name='messages_trash'),
]
