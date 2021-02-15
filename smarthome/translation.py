from modeltranslation.translator import translator, TranslationOptions
from .models import Firmware,Category,PrivacyIssue,Vulnerability,FundamentalsEntry



class FirmwareTranslationOptions(TranslationOptions):
    fields = ("changelog",)

class CategoryTranslationOptions(TranslationOptions):
    fields = ("category",)


class PrivacyIssueTranslationOptions(TranslationOptions):
    fields = ("description",)

class VulnerabilityTranslationOptions(TranslationOptions):
    fields = ("description",)


class FundamentalsEntryTranslationOptions(TranslationOptions):
    fields = ("title","text")



translator.register(Firmware,FirmwareTranslationOptions)
translator.register(Category,CategoryTranslationOptions)
translator.register(PrivacyIssue,PrivacyIssueTranslationOptions)
translator.register(Vulnerability,VulnerabilityTranslationOptions)
translator.register(FundamentalsEntry,FundamentalsEntryTranslationOptions)
