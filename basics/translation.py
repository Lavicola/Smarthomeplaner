from modeltranslation.translator import translator, TranslationOptions
from .models import FundamentalsEntry


class FundamentalsEntryTranslationOptions(TranslationOptions):
    fields = ("title","text")



translator.register(FundamentalsEntry,FundamentalsEntryTranslationOptions)
