"""
WSGI config for Django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
import rollbar
from rollbar.contrib.django.middleware import RollbarNotifierMiddleware
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "star_burger.settings")
application = get_wsgi_application()

rollbar.init(
    access_token=settings.ROLLBAR['access_token'],
    environment=settings.ROLLBAR['environment'],
    root=settings.ROLLBAR['root'],
)
