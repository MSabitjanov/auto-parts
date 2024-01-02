from modeltranslation.translator import translator, TranslationOptions

from .models import AutoPartsCategory, AutoParts, Brand


class AutoPartsCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


class AutoPartsTranslationOptions(TranslationOptions):
    fields = ("name",)


class BrandTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(AutoPartsCategory, AutoPartsCategoryTranslationOptions)
translator.register(AutoParts, AutoPartsTranslationOptions)
translator.register(Brand, BrandTranslationOptions)