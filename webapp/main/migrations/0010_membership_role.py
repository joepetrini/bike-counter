# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20140321_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.CharField(default='member', max_length=15, choices=[('member', 'member'), ('staff', 'staff'), ('admin', 'admin')]),
            preserve_default=True,
        ),
    ]
