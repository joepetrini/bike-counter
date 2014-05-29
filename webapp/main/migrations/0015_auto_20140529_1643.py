# encoding: utf8
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20140402_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(to_field=u'id', blank=True, to=settings.AUTH_USER_MODEL, help_text='Leave blank for unassigned', null=True),
        ),
    ]
