from modeltranslation.translator import translator, TranslationOptions
from configurator.models import Firmware



class FirmwareTranslationOptions(TranslationOptions):
    fields = ("changelog",)


translator.register(Firmware,FirmwareTranslationOptions)

