# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValueSet',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('name', models.CharField(max_length=25)),
                ('system_name', models.SlugField(unique=True, max_length=25)),
            ],
            options={
                u'db_table': 'value_set',
            },
            bases=(models.Model,),
        ),
    ]
