from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import translation

from .models import Haber


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
        return [(haber, lang_code) for haber in Haber.objects.all() for lang_code in ("tr", "en")]

    def location(self, item):
        haber, lang_code = item
        with translation.override(lang_code):
            return haber.get_absolute_url()

    def lastmod(self, item):
        haber, _lang_code = item
        return haber.yayin_tarihi


sitemaps = {
    "static": StaticViewSitemap,
    "haberler": HaberSitemap,
}
