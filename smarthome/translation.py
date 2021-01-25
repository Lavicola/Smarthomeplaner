from modeltranslation.translator import translator, TranslationOptions
from .models import Firmware



class FirmwareTranslationOptions(TranslationOptions):
    fields = ("changelog",)


translator.register(Firmware,FirmwareTranslationOptions)

