# ana_sayfa/urls.py
from django.urls import path
from . import views # views.py dosyasındaki fonksiyonları içeri aktardık

urlpatterns = [
    # Siteye gelen ilk isteği ('') ana_sayfa_view fonksiyonuna yönlendirir.
    path('', views.ana_sayfa_view, name='ana_sayfa'),
    path('hakkimizda/', views.hakkimizda_view, name='hakkimizda'),
    path('calisma-alanlari/', views.calisma_alanlari_view, name='calisma_alanlari'),
    path('ekibimiz/', views.ekibimiz_view, name='ekibimiz'),
    path('iletisim/', views.iletisim_view, name='iletisim'),

    # Yeni Blog/Haberler URL'leri
    path('haberler/', views.haberler_view, name='haberler'),
    path('haberler/<slug:slug>/', views.haber_detay_view, name='haber_detay'), # Detay sayfası
]