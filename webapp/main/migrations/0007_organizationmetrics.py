# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_appointment_metric'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationMetrics',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('organization', models.ForeignKey(to='main.Organization', to_field=u'id')),
                ('metric', models.ForeignKey(to='main.Metric', to_field=u'id')),
            ],
            options={
                u'unique_together': set([('organization', 'metric')]),
                u'db_table': 'org_metrics',
            },
            bases=(models.Model,),
        ),
    ]
