# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20140630_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='time_taken',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
