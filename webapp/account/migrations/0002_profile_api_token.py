# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='api_token',
            field=models.CharField(default='notarealtoken', max_length=255),
            preserve_default=False,
        ),
    ]
