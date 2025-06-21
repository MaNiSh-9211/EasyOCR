"""
WSGI config for OCRtesrect project - Root level for Vercel
"""

import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OCRtesrect.settings_production')

application = get_wsgi_application() 