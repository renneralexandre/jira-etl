"""
WSGI config for jira_etl_django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jira_etl_django_project.settings')

application = get_wsgi_application()
