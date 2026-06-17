# ana_sayfa/models.py
from django.db import models
from django.urls import reverse

class UzmanlikAlani(models.Model):
    baslik = models.CharField(max_length=100)
    aciklama = models.TextField()

    class Meta:
        verbose_name_plural = "Uzmanlık Alanları"

    def __str__(self):
        return self.baslik

class Avukat(models.Model):
    ad_soyad = models.CharField(max_length=100)
    unvan = models.CharField(max_length=100, help_text="Örn: Kurucu Avukat, Avukat")
    biyografi = models.TextField()
    fotograf = models.ImageField(upload_to='avukat_fotolari/', null=True, blank=True)
    uzmanlik_alanlari = models.ManyToManyField(UzmanlikAlani, related_name='avukatlar')

    class Meta:
        verbose_name_plural = "Avukatlar"

    def __str__(self):
        return self.ad_soyad

# ana_sayfa/models.py (En alta ekleyin)

class Iletisim(models.Model):
    ad_soyad = models.CharField(max_length=100)
    eposta = models.EmailField()
    konu = models.CharField(max_length=150)
    mesaj = models.TextField()
    gonderme_tarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "İletişim Mesajları"

    def __str__(self):
        return f'{self.ad_soyad} - {self.konu}'

class Haber(models.Model):
    baslik = models.CharField(max_length=200, verbose_name="Haber/Karar Başlığı")
    ozet = models.TextField(verbose_name="Kısa Özet")
    icerik = models.TextField(verbose_name="Haber İçeriği / Karar Metni")
    yayin_tarihi = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=150, verbose_name="URL Adresi")

    class Meta:
        verbose_name_plural = "Haberler ve Kararlar"
        ordering = ['-yayin_tarihi'] # En son eklenen en başta görünür

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        # Detay sayfasına yönlendirme için
        return reverse('haber_detay', args=[self.slug])
