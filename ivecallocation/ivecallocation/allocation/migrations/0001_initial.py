# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Application'
        db.create_table('allocation_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('project_summary', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('priority_area_radio_astronomy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority_area_geosciences', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority_area_directors', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority_area_partner', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority_area_national', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('research_record', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True, blank=True)),
            ('research_significance', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True, blank=True)),
            ('computational_methodology', self.gf('django.db.models.fields.CharField')(max_length=5000, null=True, blank=True)),
            ('core_hours_requested', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hours_allocated', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('storage_temporary', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('storage_resident', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('storage_pbstore', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('data_transfers', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('ldap_project_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='application_creators', null=True, to=orm['auth.User'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('allocation', ['Application'])

        # Adding model 'ReviewerScore'
        db.create_table('allocation_reviewerscore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('research_merit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('computational_merit', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviewerscore_reviewers', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('allocation', ['ReviewerScore'])

        # Adding model 'ReviewerComment'
        db.create_table('allocation_reviewercomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('reviewer_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reviewer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reviewercomment_reviewers', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('allocation', ['ReviewerComment'])

        # Adding model 'ResearchClassification'
        db.create_table('allocation_researchclassification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('percentage', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['ResearchClassification'])

        # Adding model 'FieldOfResearchCode'
        db.create_table('allocation_fieldofresearchcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['FieldOfResearchCode'])

        # Adding model 'ParticipantStatus'
        db.create_table('allocation_participantstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['ParticipantStatus'])

        # Adding model 'Participant'
        db.create_table('allocation_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('department_institute', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('student', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('eft', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.ParticipantStatus'])),
            ('account_email_hash', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('account_email_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('details_filled_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('account_created_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('account_created_email_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['Participant'])

        # Adding model 'Institution'
        db.create_table('allocation_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('ldap_ou_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('allocation', ['Institution'])

        # Adding model 'ParticipantAccount'
        db.create_table('allocation_participantaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['allocation.Participant'], unique=True)),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Institution'], null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('uid_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gid_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('password_hash', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('old_ldap_details', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('data_fetched_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['ParticipantAccount'])

        # Adding model 'Publication'
        db.create_table('allocation_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['Publication'])

        # Adding model 'ResearchFunding'
        db.create_table('allocation_researchfunding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('participant', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('funding_source', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('years', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('total_funding', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['ResearchFunding'])

        # Adding model 'SupportingFunding'
        db.create_table('allocation_supportingfunding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('participant', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('funding_source', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('years', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('total_funding', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['SupportingFunding'])

        # Adding model 'SupercomputerJob'
        db.create_table('allocation_supercomputerjob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('job_type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('processes', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('processes_per_node', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wallclock_time_per_job', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('number_of_type_of_job', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_memory', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('data_transfer', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['SupercomputerJob'])

        # Adding model 'Library'
        db.create_table('allocation_library', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allocation.Application'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('licensing', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('allocation', ['Library'])


    def backwards(self, orm):
        
        # Deleting model 'Application'
        db.delete_table('allocation_application')

        # Deleting model 'ReviewerScore'
        db.delete_table('allocation_reviewerscore')

        # Deleting model 'ReviewerComment'
        db.delete_table('allocation_reviewercomment')

        # Deleting model 'ResearchClassification'
        db.delete_table('allocation_researchclassification')

        # Deleting model 'FieldOfResearchCode'
        db.delete_table('allocation_fieldofresearchcode')

        # Deleting model 'ParticipantStatus'
        db.delete_table('allocation_participantstatus')

        # Deleting model 'Participant'
        db.delete_table('allocation_participant')

        # Deleting model 'Institution'
        db.delete_table('allocation_institution')

        # Deleting model 'ParticipantAccount'
        db.delete_table('allocation_participantaccount')

        # Deleting model 'Publication'
        db.delete_table('allocation_publication')

        # Deleting model 'ResearchFunding'
        db.delete_table('allocation_researchfunding')

        # Deleting model 'SupportingFunding'
        db.delete_table('allocation_supportingfunding')

        # Deleting model 'SupercomputerJob'
        db.delete_table('allocation_supercomputerjob')

        # Deleting model 'Library'
        db.delete_table('allocation_library')


    models = {
        'allocation.application': {
            'Meta': {'object_name': 'Application'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'computational_methodology': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'core_hours_requested': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'application_creators'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data_transfers': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'hours_allocated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ldap_project_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'priority_area_directors': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priority_area_geosciences': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priority_area_national': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priority_area_partner': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'priority_area_radio_astronomy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project_summary': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'project_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'research_record': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'research_significance': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'null': 'True', 'blank': 'True'}),
            'storage_pbstore': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'storage_resident': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'storage_temporary': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'allocation.fieldofresearchcode': {
            'Meta': {'object_name': 'FieldOfResearchCode'},
            'code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'allocation.institution': {
            'Meta': {'object_name': 'Institution'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ldap_ou_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'allocation.library': {
            'Meta': {'object_name': 'Library'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licensing': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'allocation.participant': {
            'Meta': {'object_name': 'Participant'},
            'account': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'account_created_email_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'account_created_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'account_email_hash': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'account_email_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'department_institute': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'details_filled_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'eft': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.ParticipantStatus']"}),
            'student': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'allocation.participantaccount': {
            'Meta': {'object_name': 'ParticipantAccount'},
            'data_fetched_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'gid_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Institution']", 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'old_ldap_details': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'participant': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['allocation.Participant']", 'unique': 'True'}),
            'password_hash': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'uid_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'allocation.participantstatus': {
            'Meta': {'object_name': 'ParticipantStatus'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'allocation.publication': {
            'Meta': {'object_name': 'Publication'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'allocation.researchclassification': {
            'Meta': {'object_name': 'ResearchClassification'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'allocation.researchfunding': {
            'Meta': {'object_name': 'ResearchFunding'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'funding_source': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'total_funding': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'years': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'allocation.reviewercomment': {
            'Meta': {'object_name': 'ReviewerComment'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviewercomment_reviewers'", 'null': 'True', 'to': "orm['auth.User']"}),
            'reviewer_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'allocation.reviewerscore': {
            'Meta': {'object_name': 'ReviewerScore'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'computational_merit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'research_merit': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reviewerscore_reviewers'", 'null': 'True', 'to': "orm['auth.User']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'allocation.supercomputerjob': {
            'Meta': {'object_name': 'SupercomputerJob'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'data_transfer': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'number_of_type_of_job': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'processes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'processes_per_node': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_memory': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'wallclock_time_per_job': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        'allocation.supportingfunding': {
            'Meta': {'object_name': 'SupportingFunding'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allocation.Application']"}),
            'funding_source': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'total_funding': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'years': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['allocation']
