# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/root/duna_trips/trip_admin')
sys.path.insert(1, '/root/duna_trips/trip_admin/my_venv/lib/python3.10/site-packages/django/__ini>
os.environ['DJANGO_SETTINGS_MODULE'] = 'trip_admin.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
