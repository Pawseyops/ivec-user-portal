# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User,Permission

class Migration(DataMigration):

    def forwards(self, orm):
            
        # and default groups
        groups = ('reviewers_astronomy', 'reviewers_directors', 'reviewers_geosciences', 'reviewers_national',
                  'reviewers_partner','privileged_reviewers', 'directors', 'unprivileged')
        for name in groups:
            orm['auth.group'](name=name).save()
            
        # add a bunch of default users and give them default groups
        users = (('admin', 'admin', True, True, True),
                 ('user', 'user', True, True, False),
                 ('reviewer', 'reviewer', True, True, False),
                 ('director', 'director', True, True, False))
        
        for username, password, is_active, is_staff, is_superuser in users:    
            # use the current ORM version to hash the user password
            u = User()
            u.set_password(password)
            password = u.password
            # now add the user and give them group membership
            u = orm['auth.user'](username=username, password=password, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser)
            u.save()
            u.groups.add(orm['auth.group'].objects.get(name='unprivileged'))
            for group in groups:
                if group[:10] == 'reviewers_': u.groups.add(orm['auth.group'].objects.get(name=group))
            u.save()
        orm['auth.user'].objects.get(username='director').groups.add(orm['auth.group'].objects.get(name='directors'))
        
        # At this stage, syncdb has been run, but skipped for the allocation app.
        # This means it will not have implicitly created the auth_permission and django_content_type records
        # for the allocation app. South resends these signals to make this happen, but only does so *after*
        # processing these migrations. Doing this seems to override that and make it work. It's needed here
        # only because permissions fixtures are being added to support a feature.
        db.really_send_create_signal('allocation', ['ReviewerScore'])
        
        # set up group permissions
        # (see the bottom of this file - exported straight from a postgres installation, not efficient, but saved on typing!)
        for group, permission in self.permissions:
            #print "Granting %s permission to group %s"%(permission, group)
            g = orm['auth.group'].objects.get(name=group)
            g.permissions.add(orm['auth.permission'].objects.get(codename=permission))
            g.save()
            
            
        # default participant statuses
        statuses = (('New', 'Created as part of an application'),
                    ('Account Email Sent', 'An account creation email has been sent to the participant'),
                    ('Account Details Filled', 'The participant has filled in all the details needed to create the account'),
                    ('Account Created', 'The account has been created for the participant'),
                    ('Account Created Email Sent', 'The account creation notification email has been sent to the participant'))
        for name, description in statuses:
            orm.ParticipantStatus(name=name, description=description).save()
        
        # add default institutions
        institutions = (('CSIRO', 'CSIRO'),
                        ('Curtin University', 'Curtin University'),
                        ('Edith Cowan University', 'Edith Cowan University'),
                        ('iVEC', 'iVEC'),
                        ('Murdoch University', 'Murdoch University'),
                        ('University of Western Australia', 'University of Western Australia'),
                        ('External', 'National'))
        for display_name, ldap_ou_name in institutions:
            orm.Institution(display_name=display_name, ldap_ou_name=ldap_ou_name).save()
            
        # add some test applications
        orm.Application(project_title='Test Application #1', project_summary='Just a test application').save()
        orm.Application(project_title='Another test application!', project_summary='Another default test application').save()
        

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
    
    permissions = (
        ('privileged_reviewers', 'add_reviewerscore'),
        ('privileged_reviewers', 'change_reviewerscore'),
        ('privileged_reviewers', 'add_reviewercomment'),
        ('privileged_reviewers', 'change_reviewercomment'),
        ('reviewers_astronomy', 'add_application'),
        ('reviewers_astronomy', 'change_application'),
        ('reviewers_astronomy', 'delete_application'),
        ('reviewers_astronomy', 'add_participant'),
        ('reviewers_astronomy', 'change_participant'),
        ('reviewers_astronomy', 'delete_participant'),
        ('reviewers_astronomy', 'add_researchfunding'),
        ('reviewers_astronomy', 'change_researchfunding'),
        ('reviewers_astronomy', 'delete_researchfunding'),
        ('reviewers_astronomy', 'add_supercomputerjob'),
        ('reviewers_astronomy', 'change_supercomputerjob'),
        ('reviewers_astronomy', 'delete_supercomputerjob'),
        ('reviewers_astronomy', 'add_researchclassification'),
        ('reviewers_astronomy', 'change_researchclassification'),
        ('reviewers_astronomy', 'delete_researchclassification'),
        ('reviewers_astronomy', 'add_fieldofresearchcode'),
        ('reviewers_astronomy', 'change_fieldofresearchcode'),
        ('reviewers_astronomy', 'delete_fieldofresearchcode'),
        ('reviewers_astronomy', 'add_publication'),
        ('reviewers_astronomy', 'change_publication'),
        ('reviewers_astronomy', 'delete_publication'),
        ('reviewers_astronomy', 'add_library'),
        ('reviewers_astronomy', 'change_library'),
        ('reviewers_astronomy', 'delete_library'),
        ('reviewers_astronomy', 'add_supportingfunding'),
        ('reviewers_astronomy', 'change_supportingfunding'),
        ('reviewers_astronomy', 'delete_supportingfunding'),
        ('reviewers_directors', 'add_application'),
        ('reviewers_directors', 'change_application'),
        ('reviewers_directors', 'delete_application'),
        ('reviewers_directors', 'add_participant'),
        ('reviewers_directors', 'change_participant'),
        ('reviewers_directors', 'delete_participant'),
        ('reviewers_directors', 'add_researchfunding'),
        ('reviewers_directors', 'change_researchfunding'),
        ('reviewers_directors', 'delete_researchfunding'),
        ('reviewers_directors', 'add_supercomputerjob'),
        ('reviewers_directors', 'change_supercomputerjob'),
        ('reviewers_directors', 'delete_supercomputerjob'),
        ('reviewers_directors', 'add_researchclassification'),
        ('reviewers_directors', 'change_researchclassification'),
        ('reviewers_directors', 'delete_researchclassification'),
        ('reviewers_directors', 'add_fieldofresearchcode'),
        ('reviewers_directors', 'change_fieldofresearchcode'),
        ('reviewers_directors', 'delete_fieldofresearchcode'),
        ('reviewers_directors', 'add_publication'),
        ('reviewers_directors', 'change_publication'),
        ('reviewers_directors', 'delete_publication'),
        ('reviewers_directors', 'add_library'),
        ('reviewers_directors', 'change_library'),
        ('reviewers_directors', 'delete_library'),
        ('reviewers_directors', 'add_supportingfunding'),
        ('reviewers_directors', 'change_supportingfunding'),
        ('reviewers_directors', 'delete_supportingfunding'),
        ('reviewers_geosciences', 'add_application'),
        ('reviewers_geosciences', 'change_application'),
        ('reviewers_geosciences', 'delete_application'),
        ('reviewers_geosciences', 'add_participant'),
        ('reviewers_geosciences', 'change_participant'),
        ('reviewers_geosciences', 'delete_participant'),
        ('reviewers_geosciences', 'add_researchfunding'),
        ('reviewers_geosciences', 'change_researchfunding'),
        ('reviewers_geosciences', 'delete_researchfunding'),
        ('reviewers_geosciences', 'add_supercomputerjob'),
        ('reviewers_geosciences', 'change_supercomputerjob'),
        ('reviewers_geosciences', 'delete_supercomputerjob'),
        ('reviewers_geosciences', 'add_researchclassification'),
        ('reviewers_geosciences', 'change_researchclassification'),
        ('reviewers_geosciences', 'delete_researchclassification'),
        ('reviewers_geosciences', 'add_fieldofresearchcode'),
        ('reviewers_geosciences', 'change_fieldofresearchcode'),
        ('reviewers_geosciences', 'delete_fieldofresearchcode'),
        ('reviewers_geosciences', 'add_publication'),
        ('reviewers_geosciences', 'change_publication'),
        ('reviewers_geosciences', 'delete_publication'),
        ('reviewers_geosciences', 'add_library'),
        ('reviewers_geosciences', 'change_library'),
        ('reviewers_geosciences', 'delete_library'),
        ('reviewers_geosciences', 'add_supportingfunding'),
        ('reviewers_geosciences', 'change_supportingfunding'),
        ('reviewers_geosciences', 'delete_supportingfunding'),
        ('reviewers_national', 'add_application'),
        ('reviewers_national', 'change_application'),
        ('reviewers_national', 'delete_application'),
        ('reviewers_national', 'add_participant'),
        ('reviewers_national', 'change_participant'),
        ('reviewers_national', 'delete_participant'),
        ('reviewers_national', 'add_researchfunding'),
        ('reviewers_national', 'change_researchfunding'),
        ('reviewers_national', 'delete_researchfunding'),
        ('reviewers_national', 'add_supercomputerjob'),
        ('reviewers_national', 'change_supercomputerjob'),
        ('reviewers_national', 'delete_supercomputerjob'),
        ('reviewers_national', 'add_researchclassification'),
        ('reviewers_national', 'change_researchclassification'),
        ('reviewers_national', 'delete_researchclassification'),
        ('reviewers_national', 'add_fieldofresearchcode'),
        ('reviewers_national', 'change_fieldofresearchcode'),
        ('reviewers_national', 'delete_fieldofresearchcode'),
        ('reviewers_national', 'add_publication'),
        ('reviewers_national', 'change_publication'),
        ('reviewers_national', 'delete_publication'),
        ('reviewers_national', 'add_library'),
        ('reviewers_national', 'change_library'),
        ('reviewers_national', 'delete_library'),
        ('reviewers_national', 'add_supportingfunding'),
        ('reviewers_national', 'change_supportingfunding'),
        ('reviewers_national', 'delete_supportingfunding'),
        ('reviewers_partner', 'add_application'),
        ('reviewers_partner', 'change_application'),
        ('reviewers_partner', 'delete_application'),
        ('reviewers_partner', 'add_participant'),
        ('reviewers_partner', 'change_participant'),
        ('reviewers_partner', 'delete_participant'),
        ('reviewers_partner', 'add_researchfunding'),
        ('reviewers_partner', 'change_researchfunding'),
        ('reviewers_partner', 'delete_researchfunding'),
        ('reviewers_partner', 'add_supercomputerjob'),
        ('reviewers_partner', 'change_supercomputerjob'),
        ('reviewers_partner', 'delete_supercomputerjob'),
        ('reviewers_partner', 'add_researchclassification'),
        ('reviewers_partner', 'change_researchclassification'),
        ('reviewers_partner', 'delete_researchclassification'),
        ('reviewers_partner', 'add_fieldofresearchcode'),
        ('reviewers_partner', 'change_fieldofresearchcode'),
        ('reviewers_partner', 'delete_fieldofresearchcode'),
        ('reviewers_partner', 'add_publication'),
        ('reviewers_partner', 'change_publication'),
        ('reviewers_partner', 'delete_publication'),
        ('reviewers_partner', 'add_library'),
        ('reviewers_partner', 'change_library'),
        ('reviewers_partner', 'delete_library'),
        ('reviewers_partner', 'add_supportingfunding'),
        ('reviewers_partner', 'change_supportingfunding'),
        ('reviewers_partner', 'delete_supportingfunding'),
        ('unprivileged', 'add_application'),
        ('unprivileged', 'change_application'),
        ('unprivileged', 'delete_application'),
    )
