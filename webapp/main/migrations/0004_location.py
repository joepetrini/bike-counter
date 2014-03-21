# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('organization', models.ForeignKey(to='main.Organization', to_field=u'id')),
                ('name', models.CharField(max_length=80)),
                ('longitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('latitude', models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True)),
                ('has_east', models.BooleanField(default=True)),
                ('has_north', models.BooleanField(default=True)),
                ('has_south', models.BooleanField(default=True)),
                ('has_west', models.BooleanField(default=True)),
            ],
            options={
                u'db_table': 'location',
            },
            bases=(models.Model,),
        ),
    ]
