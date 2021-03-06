# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('city', models.CharField(max_length=25, null=True, blank=True)),
                ('state', models.CharField(max_length=25, null=True, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=15)),
                ('member_count', models.IntegerField(null=True, blank=True)),
            ],
            options={
                u'db_table': 'organization',
            },
            bases=(models.Model,),
        ),
    ]
