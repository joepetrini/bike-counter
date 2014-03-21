# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_organizationmetrics'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('appointment', models.ForeignKey(to='main.Appointment', to_field=u'id')),
                ('is_bicycle', models.BooleanField(default=True)),
                ('longitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
            ],
            options={
                u'db_table': 'survey',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('value_set', models.ForeignKey(to='main.ValueSet', to_field=u'id')),
                ('stored_value', models.CharField(max_length=25)),
                ('display_value', models.CharField(max_length=25)),
                ('is_default', models.BooleanField(default=False)),
            ],
            options={
                u'db_table': 'value',
            },
            bases=(models.Model,),
        ),
    ]
