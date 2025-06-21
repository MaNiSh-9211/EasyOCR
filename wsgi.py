"""
WSGI config for OCRtesrect project - Root level for Vercel
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OCRtesrect.settings_production')

from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Get the WSGI application
application = get_wsgi_application()

# Wrap with StaticFilesHandler for development
if os.environ.get('DEBUG', 'False').lower() == 'true':
    application = StaticFilesHandler(application)

# Vercel requires 'app' variable
app = application 