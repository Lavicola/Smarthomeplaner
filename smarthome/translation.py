from modeltranslation.translator import translator, TranslationOptions
from .models import Firmware,DataProtectionInformation,Vulnerability,Connector

# localization of database tables

class FirmwareTranslationOptions(TranslationOptions):
    fields = ("changelog",)


class DataProtectionInformationTranslationOptions(TranslationOptions):
    fields = ("description",)

class VulnerabilityTranslationOptions(TranslationOptions):
    fields = ("description",)

class ConnectorTranslationOptions(TranslationOptions):
    fields = ("connector",)





translator.register(Firmware,FirmwareTranslationOptions)
translator.register(DataProtectionInformation,DataProtectionInformationTranslationOptions)
translator.register(Vulnerability,VulnerabilityTranslationOptions)
translator.register(Connector,ConnectorTranslationOptions)
