from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AvatarConfig(AppConfig):
    name = 'gabis.libs.avatar'
    verbose_name = _('Avatar')
    
    