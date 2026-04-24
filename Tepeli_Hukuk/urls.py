# Tepeli_Hukuk/urls.py (NİHAİ VE GÜVENLİ HALİ)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns # i18n'i kullanmak için

# 1. TEMEL URL'ler (Sadece i18n endpoint'ini içerir)
urlpatterns = [
    # Dil değiştirme mekanizması için zorunlu URL
    path('i18n/', include('django.conf.urls.i18n')), 
]

# 2. DİL ÖNEKİ GEREKEN URL'ler (Tüm site sayfaları)
# Bütün bu yollar, seçilen dile göre /tr/ veya /en/ önekini alır
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls), # Admin paneli
    path('', include('ana_sayfa.urls')), # Ana uygulamanın tüm yolları
)

# 3. MEDYA VE STATİK DOSYA URL'leri (Sadece DEBUG modunda çalışır)
# Bu kod, canlı sunucuda (DEBUG=False iken) otomatik olarak devre dışı kalır.
if settings.DEBUG:
    # Statik (CSS, JS, Bannerlar) dosyalar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
    
    # Medya (Avukat Fotoğrafları, Kullanıcı Yüklemeleri) dosyaları
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)