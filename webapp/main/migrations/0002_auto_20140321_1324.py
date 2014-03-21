# encoding: utf8
from django.db import models, migrations


def create_first_org(apps, schema_editor):
    Org = apps.get_model('main', 'Organization')
    org, created = Org.objects.get_or_create(name="Philly Bike Coalition", slug="phl-bike")


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_first_org)
    ]
