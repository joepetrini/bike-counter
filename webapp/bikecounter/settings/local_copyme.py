"""
Copy this file to local.py and update any local specific settings
It is not tracked in source control.
"""

import os
from .base import BASE_DIR

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

