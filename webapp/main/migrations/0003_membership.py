# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20140321_1324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('organization', models.ForeignKey(to='main.Organization', to_field=u'id')),
            ],
            options={
                u'unique_together': set([('user', 'organization')]),
                u'db_table': 'membership',
            },
            bases=(models.Model,),
        ),
    ]
