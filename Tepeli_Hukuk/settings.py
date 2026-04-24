"""
Django settings for Tepeli_Hukuk project.
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- GÜVENLİK VE ORTAM AYARLARI (CRITICAL FOR DEPLOYMENT) ---

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xh2+jeq1v*f49n2-^c$u=x+a&to6ezw8jkyhb4t@65iq_f_#)_'

# Canlıya alırken: DEBUG = False yapılmalı!
DEBUG = False

# Canlıya alırken: Alan adları ve IP adresi buraya eklenmeli!
ALLOWED_HOSTS = ["*"]

#ALLOWED_HOSTS = ['tepelihukuk.com', 'www.tepelihukuk.com', 'sunucunuzun_ip_adresi','localhost','10.0.2.15',]


# --- UYGULAMA TANIMLARI ---

INSTALLED_APPS = [
    # Modeltranslation, uygulamanızdan önce gelmeli
    'modeltranslation',
    'ana_sayfa',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Dil middleware'i (i18n) zorunludur
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Tepeli_Hukuk.urls'

# --- ŞABLON VE DİL AYARLARI ---

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Çeviri dosyalarının bulunduğu klasör
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

WSGI_APPLICATION = 'Tepeli_Hukuk.wsgi.application'

# --- VERİTABANI VE PAROLA DOĞRULAMA ---

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql', # POSTGRESQL MOTORU
#        'NAME': 'tepelihukuk_db',                  # CANLI ORTAM VERİTABANI ADI
#        'USER': 'tepelihukuk',                     # POSTGRESQL KULLANICI ADI
#        'PASSWORD': 'tepelihukuk1912',             # POSTGRESQL ŞİFRESİ
#        'HOST': 'localhost',                       # PostgreSQL genellikle aynı sunucudadır
#        'PORT': '5432',                            # PostgreSQL'in standart portu
#    }
#}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# --- ULUSLARARASI VE DİL AYARLARI (i18n) ---

LANGUAGE_CODE = 'tr' # Varsayılan dil
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Desteklenen Diller
LANGUAGES = [
    ('tr', _('Türkçe')),
    ('en', _('English'))
]


# --- STATİK VE MEDYA DOSYA AYARLARI (DEPLOYMENT) ---

# Statik dosyaların URL öneki (CSS, JS, Banner)
STATIC_URL = 'static/'

# Ek statik dosyaların (bizim kendi 'static/' klasörümüz) dizinleri
STATICFILES_DIRS = [BASE_DIR / 'static',]

# Canlıda collectstatic komutuyla dosyaların toplanacağı dizin (Nginx'e sunulacak klasör)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Medya Ayarları (Kullanıcı tarafından yüklenen dosyalar/Avukat Fotoğrafları)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- GENEL AYARLAR ---

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sadece geliştirme ortamında Gettext'i PATH'e ekle (Çeviri komutları için)
if DEBUG:
    GETTEXT_DIR = r'C:\Program Files\Git\usr\bin' # Sizin bilgisayarınızdaki yol
    if os.path.isdir(GETTEXT_DIR):
        os.environ['PATH'] += os.pathsep + GETTEXT_DIR
