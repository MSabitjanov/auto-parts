from modeltranslation.translator import TranslationOptions, translator
from .models import Master


class MasterTranslationOptions(TranslationOptions):
    fields = ("description",)


translator.register(Master, MasterTranslationOptions)
