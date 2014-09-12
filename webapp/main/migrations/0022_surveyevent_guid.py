# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20140911_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyevent',
            name='guid',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
    ]
