# delete_payments.py

import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(project_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monthlyfees.settings')
django.setup()

from institute_panel.models import Payment

# Delete all Payment objects
Payment.objects.all().delete()
