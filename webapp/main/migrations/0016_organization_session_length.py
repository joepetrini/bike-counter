# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20140529_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='session_length',
            field=models.IntegerField(default=90),
            preserve_default=True,
        ),
    ]
