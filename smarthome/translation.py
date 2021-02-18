from modeltranslation.translator import translator, TranslationOptions
from .models import Firmware,Category,PrivacyConcern,Vulnerability,Connector



class FirmwareTranslationOptions(TranslationOptions):
    fields = ("changelog",)

class CategoryTranslationOptions(TranslationOptions):
    fields = ("category",)


class PrivacyConcernTranslationOptions(TranslationOptions):
    fields = ("description",)

class VulnerabilityTranslationOptions(TranslationOptions):
    fields = ("description",)

class ConnectorTranslationOptions(TranslationOptions):
    fields = ("connector",)





translator.register(Firmware,FirmwareTranslationOptions)
translator.register(Category,CategoryTranslationOptions)
translator.register(PrivacyConcern,PrivacyConcernTranslationOptions)
translator.register(Vulnerability,VulnerabilityTranslationOptions)
translator.register(Connector,ConnectorTranslationOptions)