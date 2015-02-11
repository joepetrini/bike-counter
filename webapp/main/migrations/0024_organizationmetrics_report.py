# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20150106_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationmetrics',
            name='report',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
