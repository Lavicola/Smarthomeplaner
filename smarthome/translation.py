from modeltranslation.translator import translator, TranslationOptions
from .models import Firmware,PrivacyInformation,Vulnerability,Connector



class FirmwareTranslationOptions(TranslationOptions):
    fields = ("changelog",)


class PrivacyInformationTranslationOptions(TranslationOptions):
    fields = ("description",)

class VulnerabilityTranslationOptions(TranslationOptions):
    fields = ("description",)

class ConnectorTranslationOptions(TranslationOptions):
    fields = ("connector",)





translator.register(Firmware,FirmwareTranslationOptions)
translator.register(PrivacyInformation,PrivacyInformationTranslationOptions)
translator.register(Vulnerability,VulnerabilityTranslationOptions)
translator.register(Connector,ConnectorTranslationOptions)
