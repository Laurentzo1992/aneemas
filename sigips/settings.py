
from pathlib import Path
import os


if os.name == 'nt':
    VENV_BASE = os.environ['VIRTUAL_ENV']
    os.environ['PATH'] = os.path.join(VENV_BASE, 'Lib\\site-packages\\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(VENV_BASE, 'Lib\\site-packages\\osgeo\\data\\proj') + ';' + os.environ['PATH']
    
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

GEOIP_PATH = os.path.join(BASE_DIR, 'geoip/')

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "django-insecure-jm8&!s!48@8kw@hhdkj2avw)_9e-+pl_qe)^3v#$z)3*e(czzb"

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "debug_toolbar",
    "dal",
    "dal_select2",
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "crispy_forms",
    "crispy_bootstrap5",
    "commercial",
    "technique",
    "environnement",
    "paramettre",
    "authentication",
    "rest_framework",
    "corsheaders",
    "django_pandas",
    "leaflet",
    "bunsess",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "sigips.urls"


# settings.py




TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.joinpath('templates'),
            BASE_DIR.joinpath('static')
            ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sigips.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
"""

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aneemas',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
"""
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aneemas',
        'USER': 'ubuntu',
        'PASSWORD': 'pago@2023',
        'HOST': '94.23.165.51',
        'PORT': '5432',
    }
}
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sonasp',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"


STATIC_ROOT = BASE_DIR / 'static'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "sigips/static")
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "sigips/static/media")



LEAFLET_CONFIG = {

    #you can use your own

    "DEFAULT_CENTER" : (40.5, -0.09),

    "DEFAULT_ZOOM" : 1,

    "MAX_ZOOM" : 20,

    "MIN_ZOOM" : 3,

    "SCALE" : 'both',

    "ATTRIBUTION_PREFIX" : "My Custome Leaflet map"

}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

#Template conf
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = 'authentication.User'

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'home'

# Twillo credential
TWILIO_ACCOUNT_SID = 'AC15fbce0675e82420dce584d408ca97ce'

TWILIO_AUTH_TOKEN = 'ce8bc149e7b00b6253fdfff807e7a923'

# Pour retirer le slash à la fin

APPEND_SLASH=True

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10000000000000
}

X_FRAME_OPTIONS = 'SAMEORIGIN'

JET_DEFAULT_THEME = 'green'
JET_SIDE_MENU_COMPACT = True

JET_SIDE_MENU_ITEMS = {
        'gesco': [
            {'label': 'Gestion', 'app_label': 'commerical', 'items': [
                {'name': 'commercial.fichecontrol', 'label': 'Achat'},
                {'name': 'commercial.fichetarification', 'label': 'Ventes'},
                {'label': 'Paiement', 'url': "/gesco/commercial/transferedfichetarification", 'label': 'Mouvement Lingots'},
            ]}, 
            {'label': 'Parametrage', 'app_label': 'commercial', 'items': [
                {'name': 'commercial.typesubstance'},
                {'name': 'commercial.typefournisseur'},
                {'name': 'commercial.directionlingot'},
                {'name': 'commercial.emplacementlingot'},
                {'name': 'commercial.stragietarification'},
                {'name': 'commercial.modepayement'},
            ]},
        ],
        'admin1': [
            {'label': 'Paramettre', 'app_label': 'paramettre', 'items': [
                {'name': 'paramettre.burencadrements'},
                {'name': 'paramettre.categories'},
                {'name': 'paramettre.communes'},
                {'name': 'paramettre.comptoires'},
                {'name': 'paramettre.comsites'},
                {'name': 'paramettre.comzones'},
                {'name': 'paramettre.provinces'},
                {'name': 'paramettre.regions'},
                {'name': 'paramettre.statutsites'},
                {'name': 'paramettre.typaccidents'},
                {'name': 'paramettre.typautorisations'},
                {'name': 'paramettre.typdemandeurs'},
                {'name': 'paramettre.typenatureminerais'},
                {'name': 'paramettre.typenatureterrains'},
                {'name': 'paramettre.typeorganisations'},
                {'name': 'paramettre.typeproduitchimiques'},
                {'name': 'paramettre.typequipements'},
                {'name': 'paramettre.typesites'},
                {'name': 'paramettre.typetaterrains'},
                {'name': 'paramettre.typecarte'},
            ]}
        ]
    }
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


# JET_INDEX_DASHBOARD = 'commercial.dashboard_modules.CustomIndexDashboard'
# JET_INDEX_DASHBOARD = 'jet.dashboard.dashboard.CustomIndexDashboard'