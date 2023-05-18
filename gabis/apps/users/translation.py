from __future__ import unicode_literals, absolute_import

import logging

from modeltranslation.translator import translator, TranslationOptions

from gabis.apps.users.models.users import User

log = logging.getLogger(__name__)

class UserTranslationOptions(TranslationOptions):
    fields = ('name', 'birth_city', 'birth_date', 'address', 'mobile',)

translator.register(User, UserTranslationOptions)