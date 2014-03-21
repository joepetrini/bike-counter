# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_survey_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyValue',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name=u'created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name=u'modified', editable=False)),
                ('survey', models.ForeignKey(to='main.Survey', to_field=u'id')),
                ('metric', models.ForeignKey(to='main.Metric', to_field=u'id')),
                ('value', models.ForeignKey(to='main.Value', to_field=u'id')),
            ],
            options={
                u'unique_together': set([('survey', 'metric')]),
                u'db_table': 'survey_value',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='type',
            field=models.CharField(default='intersection', max_length=20, choices=[('intersection', 'Intersection'), ('trail', 'Trail'), ('bridge', 'Bridge')]),
            preserve_default=True,
        ),
    ]
