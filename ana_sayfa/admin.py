from django.contrib import admin

# ana_sayfa/admin.py
from django.contrib import admin
from .models import Avukat, UzmanlikAlani, Iletisim, Haber

# Avukatlar ve Uzmanlık Alanları için basit kayıt
admin.site.register(Avukat)
admin.site.register(UzmanlikAlani)
admin.site.register(Iletisim)

# Haber modelini kaydederken slug alanını otomatik doldurmak için
class HaberAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'yayin_tarihi')
    prepopulated_fields = {'slug': ('baslik',)} # Başlıktan slug oluşturur

admin.site.register(Haber, HaberAdmin)