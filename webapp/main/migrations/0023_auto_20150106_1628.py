# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_surveyevent_guid'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='longest_pause',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='total_away',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='total_pause',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
