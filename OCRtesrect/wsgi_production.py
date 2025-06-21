"""
WSGI config for OCRtesrect project - Production version for Vercel
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OCRtesrect.settings_production')

application = get_wsgi_application() 