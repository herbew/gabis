from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TemplatedDocsConfig(AppConfig):
    verbose_name = _('TemplatedDocs')
    name = 'gabis.libs.templated_docs'
