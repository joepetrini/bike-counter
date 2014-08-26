# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_appointment_time_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationmetrics',
            name='required',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
