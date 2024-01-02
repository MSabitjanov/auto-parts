from modeltranslation.translator import TranslationOptions, translator
from apps.users.models import Master, Seller, MasterSkill, Region


class MasterTranslationOptions(TranslationOptions):
    fields = ("description",)


class SellerTranslationOptions(TranslationOptions):
    fields = ("company_info",)


class MasterSkillTranslationOptions(TranslationOptions):
    fields = ("name",)


class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)


translator.register(Master, MasterTranslationOptions)
translator.register(Seller, SellerTranslationOptions)
translator.register(MasterSkill, MasterSkillTranslationOptions)
translator.register(Region, RegionTranslationOptions)