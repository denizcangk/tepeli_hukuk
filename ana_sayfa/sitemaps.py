from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import translation

from .karar_verileri import guncel_karar_kayitlari
from .models import Haber
from .site_verileri import HIZMET_ALANLARI


STATIC_PAGES = (
    ("ana_sayfa", 1.0),
    ("hakkimizda", 0.8),
    ("calisma_alanlari", 0.9),
    ("ekibimiz", 0.7),
    ("haberler", 0.7),
    ("iletisim", 0.9),
)


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return [(view_name, lang_code, priority) for view_name, priority in STATIC_PAGES for lang_code in ("tr", "en")]

    def location(self, item):
        view_name, lang_code, _priority = item
        with translation.override(lang_code):
            return reverse(view_name)

    def priority(self, item):
        return item[2]


class HaberSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6
    protocol = "https"

    def items(self):
        haberler = list(Haber.objects.all()) or guncel_karar_kayitlari()
        return [(haber, lang_code) for haber in haberler for lang_code in ("tr", "en")]

    def location(self, item):
        haber, lang_code = item
        with translation.override(lang_code):
            if hasattr(haber, "get_absolute_url"):
                return haber.get_absolute_url()
            return reverse("haber_detay", args=[haber.slug])

    def lastmod(self, item):
        haber, _lang_code = item
        return haber.yayin_tarihi


class CalismaAlaniSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return [(alan, lang_code) for lang_code, alanlar in HIZMET_ALANLARI.items() for alan in alanlar]

    def location(self, item):
        alan, lang_code = item
        with translation.override(lang_code):
            return reverse("calisma_alani_detay", args=[alan["slug"]])


sitemaps = {
    "static": StaticViewSitemap,
    "calisma_alanlari": CalismaAlaniSitemap,
    "haberler": HaberSitemap,
}
