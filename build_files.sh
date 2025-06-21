#!/bin/bash
# build_files.sh
pip install -r requirements.txt
python manage.py collectstatic --noinput --settings=OCRtesrect.settings_production
python manage.py migrate --settings=OCRtesrect.settings_production
python manage.py createcachetable --settings=OCRtesrect.settings_production 