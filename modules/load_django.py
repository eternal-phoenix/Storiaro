import sys
import os
import django

sys.path.append(os.path.abspath("storiaro_project"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'storiaro_project.settings'
django.setup()
