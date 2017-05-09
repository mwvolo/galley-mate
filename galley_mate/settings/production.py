# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=galley_mate.settings.production
from .base import *             # NOQA
import logging.config

# For security and performance reasons, DEBUG is turned off
DEBUG = False
TEMPLATE_DEBUG = False

# Must mention ALLOWED_HOSTS in production!
# ALLOWED_HOSTS = ["galley_mate.com"]

# Cache the templates in memory for speed-up
loaders = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0].update({"APP_DIRS": False})

# Define STATIC_ROOT for the collectstatic command
STATIC_ROOT = join(BASE_DIR, '..', 'site', 'static')
