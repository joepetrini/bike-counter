# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_organization_session_length'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': [b'name']},
        ),
    ]
