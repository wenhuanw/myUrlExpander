"""
WSGI config for myurlpro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import site
import sys
from django.core.wsgi import get_wsgi_application
site.addsitedir('/home/ubuntu/djangourl/myvenv3/lib/python3.4/site-packages')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myurlpro.settings")
sys.path.append('/home/ubuntu/djangourl/myurlpro')
application = get_wsgi_application()
