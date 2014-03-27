# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_organizationmetrics_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='system_name',
            field=models.SlugField(default='name', unique=True, max_length=25),
            preserve_default=False,
        ),
    ]
