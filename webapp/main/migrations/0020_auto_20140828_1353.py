# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_organizationmetrics_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=25)),
                ('system_name', models.SlugField(unique=True, max_length=25)),
            ],
            options={
                'db_table': 'events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrganizationEvents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('event', models.ForeignKey(to='main.Event')),
                ('organization', models.ForeignKey(to='main.Organization')),
            ],
            options={
                'db_table': 'org_events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurveyEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('longitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('appointment', models.ForeignKey(to='main.Appointment')),
                ('event', models.ForeignKey(to='main.Event')),
            ],
            options={
                'db_table': 'survey_events',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='organizationevents',
            unique_together=set([('organization', 'event')]),
        ),
    ]
