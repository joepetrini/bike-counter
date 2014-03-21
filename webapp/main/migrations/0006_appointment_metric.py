# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_valueset'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('organization', models.ForeignKey(to='main.Organization', to_field=u'id')),
                ('location', models.ForeignKey(to='main.Location', to_field=u'id')),
                ('user', models.ForeignKey(to_field=u'id', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('scheduled_start', models.DateTimeField()),
                ('actual_start', models.DateTimeField(null=True, blank=True)),
                ('actual_end', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                u'db_table': 'appointment',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('name', models.CharField(max_length=25)),
                ('desc', models.CharField(max_length=250, null=True, blank=True)),
                ('value_set', models.ForeignKey(to='main.ValueSet', to_field=u'id')),
            ],
            options={
                u'db_table': 'metric',
            },
            bases=(models.Model,),
        ),
    ]
