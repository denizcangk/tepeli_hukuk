# ana_sayfa/views.py
import json

from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _  # i18n için _() fonksiyonu
from .karar_verileri import guncel_karar_kayitlari
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

SEO_VERILERI = {
    "tr": {
        "ana_sayfa": {
            "title": "Tepeli Hukuk Bürosu | Avukatlık ve Hukuki Danışmanlık",
            "description": "Tepeli Hukuk Bürosu; bireysel ve kurumsal müvekkillerine dava takibi, sözleşmeler, iş hukuku, ticaret hukuku ve danışmanlık alanlarında hizmet verir.",
        },
        "hakkimizda": {
            "title": "Hakkımızda | Tepeli Hukuk Bürosu",
            "description": "Tepeli Hukuk Bürosu'nun çalışma anlayışı, müvekkil ilişkileri ve hukuki hizmet yaklaşımı hakkında bilgi alın.",
        },
        "calisma_alanlari": {
            "title": "Çalışma Alanlarımız | Tepeli Hukuk Bürosu",
            "description": "Tepeli Hukuk Bürosu'nun dava takibi, sözleşmeler, ticaret hukuku, iş hukuku, aile hukuku ve icra hukuku alanlarındaki hizmetlerini inceleyin.",
        },
        "ekibimiz": {
            "title": "Ekibimiz | Tepeli Hukuk Bürosu",
            "description": "Tepeli Hukuk Bürosu avukat kadrosu ve çalışma alanları hakkında bilgi alın.",
        },
        "iletisim": {
            "title": "İletişim | Tepeli Hukuk Bürosu",
            "description": "Tepeli Hukuk Bürosu ile iletişime geçin. Randevu ve hukuki danışmanlık taleplerinizi iletişim formu üzerinden iletebilirsiniz.",
        },
        "haberler": {
            "title": "Güncel Kararlar ve Hukuk Haberleri | Tepeli Hukuk Bürosu",
            "description": "Tepeli Hukuk Bürosu tarafından paylaşılan güncel kararlar, hukuki gelişmeler ve bilgilendirici içerikler.",
        },
    },
    "en": {
        "ana_sayfa": {
            "title": "Tepeli Law Firm | Legal Services and Consultancy",
            "description": "Tepeli Law Firm provides legal consultancy, litigation support, contract review and corporate legal services for individuals and companies.",
        },
        "hakkimizda": {
            "title": "About Us | Tepeli Law Firm",
            "description": "Learn about Tepeli Law Firm's professional approach, client relationships and legal service principles.",
        },
        "calisma_alanlari": {
            "title": "Practice Areas | Tepeli Law Firm",
            "description": "Explore Tepeli Law Firm's services in litigation, contracts, commercial law, employment law, family law and enforcement proceedings.",
        },
        "ekibimiz": {
            "title": "Our Team | Tepeli Law Firm",
            "description": "Learn about Tepeli Law Firm's lawyers, professional background and practice areas.",
        },
        "iletisim": {
            "title": "Contact | Tepeli Law Firm",
            "description": "Contact Tepeli Law Firm for appointment requests and legal consultancy inquiries through the contact form.",
        },
        "haberler": {
            "title": "Latest Rulings and Legal News | Tepeli Law Firm",
            "description": "Latest rulings, legal updates and informative articles shared by Tepeli Law Firm.",
        },
    },
}

FALLBACK_UZMANLIK_ALANLARI = {
    "tr": [
        {"baslik": "Ticaret ve Şirketler Hukuku", "aciklama": "Şirket kuruluşu, sözleşme hazırlığı, kurumsal danışmanlık ve ticari uyuşmazlık süreçlerinde destek."},
        {"baslik": "İş Hukuku", "aciklama": "İşçi ve işveren uyuşmazlıkları, iş sözleşmeleri, fesih süreçleri ve işçilik alacakları konusunda danışmanlık."},
        {"baslik": "Sözleşmeler Hukuku", "aciklama": "Sözleşme hazırlama, inceleme, müzakere ve sözleşmeden doğan uyuşmazlıkların çözümü."},
        {"baslik": "İcra ve Alacak Takibi", "aciklama": "Alacakların tahsili, icra takipleri, itiraz süreçleri ve borç ilişkilerinden doğan uyuşmazlıklar."},
        {"baslik": "Aile Hukuku", "aciklama": "Boşanma, velayet, nafaka, mal rejimi ve aile hukukuna ilişkin dava ve danışmanlık süreçleri."},
        {"baslik": "Gayrimenkul Hukuku", "aciklama": "Kira ilişkileri, tapu işlemleri, taşınmaz uyuşmazlıkları ve gayrimenkul sözleşmeleri."},
    ],
    "en": [
        {"baslik": "Commercial and Corporate Law", "aciklama": "Support for company formation, contract drafting, corporate consultancy and commercial disputes."},
        {"baslik": "Employment Law", "aciklama": "Consultancy on employee and employer disputes, employment contracts, termination and labor receivables."},
        {"baslik": "Contract Law", "aciklama": "Drafting, reviewing and negotiating contracts, and resolving contract-related disputes."},
        {"baslik": "Enforcement and Debt Collection", "aciklama": "Debt collection, enforcement proceedings, objections and disputes arising from debt relationships."},
        {"baslik": "Family Law", "aciklama": "Legal support for divorce, custody, alimony, matrimonial property and family law disputes."},
        {"baslik": "Real Estate Law", "aciklama": "Lease relations, title deed procedures, real estate disputes and property contracts."},
    ],
}


def aktif_dil():
    language = (get_language() or "tr").split("-")[0]
    return language if language in SEO_VERILERI else "tr"


def dil_yolu(path, lang_code):
    if path.startswith("/tr/") or path == "/tr":
        suffix = path[3:]
        return f"/{lang_code}{suffix or '/'}"
    if path.startswith("/en/") or path == "/en":
        suffix = path[3:]
        return f"/{lang_code}{suffix or '/'}"
    return f"/{lang_code}{path if path.startswith('/') else '/' + path}"


def seo_context(request, sayfa_anahtari, extra=None):
    lang_code = aktif_dil()
    seo = dict(SEO_VERILERI[lang_code][sayfa_anahtari])
    if extra:
        seo.update(extra)

    seo["canonical"] = request.build_absolute_uri(request.path)
    seo["alternates"] = {
        "tr": request.build_absolute_uri(dil_yolu(request.path, "tr")),
        "en": request.build_absolute_uri(dil_yolu(request.path, "en")),
    }

    if sayfa_anahtari == "ana_sayfa":
        seo["json_ld"] = json.dumps({
            "@context": "https://schema.org",
            "@type": "LegalService",
            "name": "Tepeli Hukuk Bürosu",
            "url": "https://tepelihukuk.com/",
            "areaServed": "Türkiye",
            "availableLanguage": ["tr", "en"],
        }, ensure_ascii=False)

    return seo


def robots_txt(_request):
    content = "User-agent: *\nAllow: /\n\nSitemap: https://tepelihukuk.com/sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")


# --- TEMEL SAYFA GÖRÜNÜMLERİ ---

def ana_sayfa_view(request):
    uzmanliklar = list(UzmanlikAlani.objects.all()) or FALLBACK_UZMANLIK_ALANLARI[aktif_dil()]
    avukatlar = Avukat.objects.all()

    context = {
        'uzmanliklar': uzmanliklar,
        'avukatlar': avukatlar,
        'sayfa': SAYFA_VERILERI['ana_sayfa'],
        'seo': seo_context(request, 'ana_sayfa'),
    }
    return render(request, 'pages/ana_sayfa.html', context)


def hakkimizda_view(request):
    context = {
        'sayfa': SAYFA_VERILERI['hakkimizda'],
        'seo': seo_context(request, 'hakkimizda'),
    }
    return render(request, 'pages/hakkimizda.html', context)  # Context düzeltildi


def calisma_alanlari_view(request):
    uzmanliklar = list(UzmanlikAlani.objects.all()) or FALLBACK_UZMANLIK_ALANLARI[aktif_dil()]
    context = {
        'uzmanliklar': uzmanliklar,
        'sayfa': SAYFA_VERILERI['calisma_alanlari'],
        'seo': seo_context(request, 'calisma_alanlari'),
    }
    return render(request, 'pages/calisma_alanlari.html', context)


def ekibimiz_view(request):
    avukatlar = Avukat.objects.all()
    context = {
        'avukatlar': avukatlar,
        'sayfa': SAYFA_VERILERI['ekibimiz'],
        'seo': seo_context(request, 'ekibimiz'),
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
        'sayfa': SAYFA_VERILERI['iletisim'],
        'seo': seo_context(request, 'iletisim'),
    }
    return render(request, 'pages/iletisim.html', context)


# --- HABERLER / BLOG GÖRÜNÜMLERİ ---

def haberler_view(request):
    haberler = list(Haber.objects.all()) or guncel_karar_kayitlari()
    context = {
        'haberler': haberler,
        'sayfa': SAYFA_VERILERI['haberler'],
        'seo': seo_context(request, 'haberler'),
    }
    return render(request, 'pages/haberler.html', context)


def haber_detay_view(request, slug):
    haber = Haber.objects.filter(slug=slug).first()
    if haber is None:
        haber = next((karar for karar in guncel_karar_kayitlari() if karar.slug == slug), None)
    if haber is None:
        raise Http404("Haber bulunamadı.")

    context = {
        'haber': haber,
        # Dinamik başlık, modelin çeviri alanını kullanmalı
        'sayfa': {'title': haber.baslik, 'banner': SAYFA_VERILERI['haberler']['banner']},
        'seo': seo_context(request, 'haberler', {
            'title': f'{haber.baslik} | Tepeli Hukuk Bürosu',
            'description': haber.ozet[:155],
        }),
    }
    return render(request, 'pages/haber_detay.html', context)
