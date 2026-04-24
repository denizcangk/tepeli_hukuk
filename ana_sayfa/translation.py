from modeltranslation.translator import translator, TranslationOptions
from .models import Avukat, Haber

# 1. AVUKAT MODELİ ÇEVİRİ ALANLARI
class AvukatTranslationOptions(TranslationOptions):
    # Bu alanlar admin panelinde TR ve EN olarak ayrı ayrı görünecek
    fields = ('unvan', 'biyografi')

# 2. HABER MODELİ ÇEVİRİ ALANLARI
class HaberTranslationOptions(TranslationOptions):
    # Blog/Karar başlıkları, özetleri ve içerikleri çevrilecek
    fields = ('baslik', 'ozet', 'icerik')

# Çeviri seçeneklerini Django'ya kaydet
translator.register(Avukat, AvukatTranslationOptions)
translator.register(Haber, HaberTranslationOptions)