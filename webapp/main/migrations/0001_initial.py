# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table('profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Profile'])

        # Adding model 'Organization'
        db.create_table('organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('members', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Organization'])

        # Adding model 'Membership'
        db.create_table('membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Organization'])),
        ))
        db.send_create_signal(u'main', ['Membership'])

        # Adding unique constraint on 'Membership', fields ['user', 'organization']
        db.create_unique('membership', ['user_id', 'organization_id'])

        # Adding model 'Location'
        db.create_table('location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Organization'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('type', self.gf('django.db.models.fields.CharField')(default='intersection', max_length=20)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('has_east', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_north', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_south', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('has_west', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'main', ['Location'])

        # Adding model 'ValueSet'
        db.create_table('valueset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'main', ['ValueSet'])

        # Adding model 'Value'
        db.create_table('value', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('valueset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ValueSet'])),
            ('stored_value', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('display_value', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'main', ['Value'])

        # Adding model 'Metric'
        db.create_table('metric', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('valueset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ValueSet'])),
        ))
        db.send_create_signal(u'main', ['Metric'])

        # Adding model 'OrganizationMetrics'
        db.create_table('org_metrics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Organization'])),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Metric'])),
        ))
        db.send_create_signal(u'main', ['OrganizationMetrics'])

        # Adding unique constraint on 'OrganizationMetrics', fields ['organization', 'metric']
        db.create_unique('org_metrics', ['organization_id', 'metric_id'])

        # Adding model 'Appointment'
        db.create_table('appointment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Organization'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Location'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('scheduled_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('actual_start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('actual_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Appointment'])

        # Adding model 'Survey'
        db.create_table('survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('appointment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Appointment'])),
            ('is_bicycle', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Survey'])

        # Adding model 'SurveyValue'
        db.create_table('surveyvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Survey'])),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Metric'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Value'])),
        ))
        db.send_create_signal(u'main', ['SurveyValue'])

        # Adding unique constraint on 'SurveyValue', fields ['survey', 'metric']
        db.create_unique('surveyvalue', ['survey_id', 'metric_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'SurveyValue', fields ['survey', 'metric']
        db.delete_unique('surveyvalue', ['survey_id', 'metric_id'])

        # Removing unique constraint on 'OrganizationMetrics', fields ['organization', 'metric']
        db.delete_unique('org_metrics', ['organization_id', 'metric_id'])

        # Removing unique constraint on 'Membership', fields ['user', 'organization']
        db.delete_unique('membership', ['user_id', 'organization_id'])

        # Deleting model 'Profile'
        db.delete_table('profile')

        # Deleting model 'Organization'
        db.delete_table('organization')

        # Deleting model 'Membership'
        db.delete_table('membership')

        # Deleting model 'Location'
        db.delete_table('location')

        # Deleting model 'ValueSet'
        db.delete_table('valueset')

        # Deleting model 'Value'
        db.delete_table('value')

        # Deleting model 'Metric'
        db.delete_table('metric')

        # Deleting model 'OrganizationMetrics'
        db.delete_table('org_metrics')

        # Deleting model 'Appointment'
        db.delete_table('appointment')

        # Deleting model 'Survey'
        db.delete_table('survey')

        # Deleting model 'SurveyValue'
        db.delete_table('surveyvalue')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.appointment': {
            'Meta': {'object_name': 'Appointment', 'db_table': "'appointment'"},
            'actual_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'actual_start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Location']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Organization']"}),
            'scheduled_start': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'main.location': {
            'Meta': {'object_name': 'Location', 'db_table': "'location'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'has_east': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_north': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_south': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'has_west': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Organization']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'intersection'", 'max_length': '20'})
        },
        u'main.membership': {
            'Meta': {'unique_together': "(('user', 'organization'),)", 'object_name': 'Membership', 'db_table': "'membership'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Organization']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'main.metric': {
            'Meta': {'object_name': 'Metric', 'db_table': "'metric'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'valueset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ValueSet']"})
        },
        u'main.organization': {
            'Meta': {'object_name': 'Organization', 'db_table': "'organization'"},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        u'main.organizationmetrics': {
            'Meta': {'unique_together': "(('organization', 'metric'),)", 'object_name': 'OrganizationMetrics', 'db_table': "'org_metrics'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Metric']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Organization']"})
        },
        u'main.profile': {
            'Meta': {'object_name': 'Profile', 'db_table': "'profile'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'main.survey': {
            'Meta': {'object_name': 'Survey', 'db_table': "'survey'"},
            'appointment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Appointment']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_bicycle': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        u'main.surveyvalue': {
            'Meta': {'unique_together': "(('survey', 'metric'),)", 'object_name': 'SurveyValue', 'db_table': "'surveyvalue'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Metric']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Survey']"}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Value']"})
        },
        u'main.value': {
            'Meta': {'object_name': 'Value', 'db_table': "'value'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'display_value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'stored_value': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'valueset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.ValueSet']"})
        },
        u'main.valueset': {
            'Meta': {'object_name': 'ValueSet', 'db_table': "'valueset'"},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['main']