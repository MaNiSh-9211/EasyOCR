#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Use development settings by default for local development
    # Set DJANGO_SETTINGS_MODULE environment variable to override
    default_settings = os.environ.get(
        'DJANGO_SETTINGS_MODULE', 
        'OCRtesrect.settings_development'
    )
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_settings)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv) 