# ana_sayfa/views.py
from django.shortcuts import render, get_object_or_404  # get_object_or_404 eklendi
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _  # i18n için _() fonksiyonu
from .models import Avukat, UzmanlikAlani, Iletisim, Haber  # Tüm modelleri içeri aktardık

# Tüm view'lerde kullanılacak statik sayfa verileri
SAYFA_VERILERI = {
    'ana_sayfa': {'title': _('Tepeli Hukuk Bürosu'), 'banner': 'default-banner.jpg'},
    'hakkimizda': {'title': _('Hukuk Büromuz Hakkında'), 'banner': 'hakkimizda-banner.jpg'},
    'calisma_alanlari': {'title': _('Çalışma Alanlarımız'), 'banner': 'calisma-banner.jpg'},
    'ekibimiz': {'title': _('Hukuk Kadromuz'), 'banner': 'ekibimiz-banner.jpg'},
    'iletisim': {'title': _('Bizimle İletişime Geçin'), 'banner': 'iletisim-banner.jpg'},
    'haberler': {'title': _('Güncel Kararlar ve Haberler'), 'banner': 'blog-banner.jpg'},
}


# --- TEMEL SAYFA GÖRÜNÜMLERİ ---

def ana_sayfa_view(request):
    uzmanliklar = UzmanlikAlani.objects.all()
    avukatlar = Avukat.objects.all()

    context = {
        'uzmanliklar': uzmanliklar,
        'avukatlar': avukatlar,
        'sayfa': SAYFA_VERILERI['ana_sayfa']
    }
    return render(request, 'pages/ana_sayfa.html', context)


def hakkimizda_view(request):
    context = {
        'sayfa': SAYFA_VERILERI['hakkimizda']
    }
    return render(request, 'pages/hakkimizda.html', context)  # Context düzeltildi


def calisma_alanlari_view(request):
    uzmanliklar = UzmanlikAlani.objects.all()
    context = {
        'uzmanliklar': uzmanliklar,
        'sayfa': SAYFA_VERILERI['calisma_alanlari']
    }
    return render(request, 'pages/calisma_alanlari.html', context)


def ekibimiz_view(request):
    avukatlar = Avukat.objects.all()
    context = {
        'avukatlar': avukatlar,
        'sayfa': SAYFA_VERILERI['ekibimiz']
    }
    return render(request, 'pages/ekibimiz.html', context)


def iletisim_view(request):
    mesaj = None
    if request.method == 'POST':
        # Gelen veriyi yakala ve Iletisim modeline kaydet
        Iletisim.objects.create(
            ad_soyad=request.POST.get('ad_soyad'),
            eposta=request.POST.get('eposta'),
            konu=request.POST.get('konu'),
            mesaj=request.POST.get('mesaj')
        )
        # Kayıt başarılı, kullanıcıyı sayfaya yönlendir ve mesaj göster
        return HttpResponseRedirect(reverse('iletisim') + '?success=true')

    # Başarı mesajı varsa context'e ekle
    if 'success' in request.GET:
        mesaj = _("Mesajınız başarıyla alınmıştır. En kısa sürede size dönüş yapılacaktır.")

    context = {
        'mesaj': mesaj,
        'sayfa': SAYFA_VERILERI['iletisim']
    }
    return render(request, 'pages/iletisim.html', context)


# --- HABERLER / BLOG GÖRÜNÜMLERİ ---

def haberler_view(request):
    haberler = Haber.objects.all()  # Tüm haberleri çek
    context = {
        'haberler': haberler,
        'sayfa': SAYFA_VERILERI['haberler']
    }
    return render(request, 'pages/haberler.html', context)


def haber_detay_view(request, slug):
    # Modelden slug ile haberi çek, bulunamazsa 404 döndür
    haber = get_object_or_404(Haber, slug=slug)

    context = {
        'haber': haber,
        # Dinamik başlık, modelin çeviri alanını kullanmalı
        'sayfa': {'title': haber.baslik, 'banner': SAYFA_VERILERI['haberler']['banner']}
    }
    return render(request, 'pages/haber_detay.html', context)