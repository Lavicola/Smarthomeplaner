from modeltranslation.translator import translator, TranslationOptions
from .models import Firmware,Category,PrivacyIssue,Vulnerability



class FirmwareTranslationOptions(TranslationOptions):
    fields = ("changelog",)

class CategoryTranslationOptions(TranslationOptions):
    fields = ("category",)


class PrivacyIssueTranslationOptions(TranslationOptions):
    fields = ("description",)

class VulnerabilityTranslationOptions(TranslationOptions):
    fields = ("description",)




translator.register(Firmware,FirmwareTranslationOptions)
translator.register(Category,CategoryTranslationOptions)
translator.register(PrivacyIssue,PrivacyIssueTranslationOptions)
translator.register(Vulnerability,VulnerabilityTranslationOptions)
