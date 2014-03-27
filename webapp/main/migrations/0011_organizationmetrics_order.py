# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_membership_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationmetrics',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
