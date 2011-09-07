# -*- coding: utf-8 -*-
import operator
from ivecallocation.allocation.models import *
from django.contrib import admin
from django import forms
from admin_forms import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.db.models import Q
from ivecallocation.allocation.utils import get_querylist
from ivecallocation.allocation import account_services
from django.http import HttpResponse

class ResearchClassificationInline(admin.TabularInline):
    model = ResearchClassification
    extra = 1

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1

class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 1
    form = PublicationForm

class ResearchFundingInline(admin.TabularInline):
    model = ResearchFunding
    extra = 1

class SupportingFundingInline(admin.TabularInline):
    model = SupportingFunding
    extra = 1    

class SupercomputerJobInline(admin.TabularInline):
    model = SupercomputerJob
    extra = 1

class LibraryInline(admin.TabularInline):
    model = Library
    extra = 1

class ReviewerScoreInline(admin.TabularInline):
    model = ReviewerScore
    fields = ['research_merit', 'computational_merit', 'reviewer']
    extra = 1
    form = ReviewerScoreForm

class ReviewerCommentInline(admin.TabularInline):
    model = ReviewerComment
    extra = 1
    form = ReviewerCommentForm

class ApplicationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['project_title', 'created_by', 'core_hours_requested', 'priority_area', 'submitted']
    list_filter = ['complete', 'priority_area_radio_astronomy', 'priority_area_geosciences', 'priority_area_directors',
                   'priority_area_partner', 'priority_area_national', 'range:hours_allocated']
    inlines = [ResearchClassificationInline, ParticipantInline, PublicationInline, ResearchFundingInline,
               SupportingFundingInline, SupercomputerJobInline, LibraryInline, ReviewerScoreInline, ReviewerCommentInline]
    form = ApplicationForm
    search_fields = ['project_title']
    actions = ['CSV_summary_of_LDAP_accounts', 'create_ldap_groups']

    fieldsets = [
        ('Part A - Summary', 
         {'fields': 
              (
              'project_title',
              'project_summary',
              ),
          }
        ),

        ('Priority Areas', 
         {'fields': 
              (
              'priority_area_radio_astronomy',
              'priority_area_geosciences',
              'priority_area_directors',
              'priority_area_partner',
              'priority_area_national',              
              ),
          'description': help_text_priority_areas
          }
        ),


        ('', 
         {'fields': 
              (
              'ResearchClassificationInline',
              ),
          'description': help_text_research_classifications
          }
        ),


        ('', 
         {'fields': 
              (
              'ParticipantInline',
              ),
          'description': help_text_project_participants
          }
        ),

        ('Part B - Project Team', 
         {'fields': 
              (
              'research_record',
              )
          }
        ),
        ('', 
         {'fields': 
              (
              'PublicationInline',
              ),
          'description': help_text_publications
          }
        ),
        ('', 
         {'fields': 
              (
              'ResearchFundingInline',
              ),
          'description': help_text_research_funding
          }
        ),




        ('Part C - Research Proposal', 
         {'fields': 
              (
              'research_significance',
              'computational_methodology',
              )
          }
        ),
        ('', 
         {'fields': 
              (
              'SupportingFundingInline',
              ),
          'description': help_text_supporting_funding
          }
        ),


        ('', 
         {'fields': 
              (
              'SupercomputerJobInline',              
              'core_hours_requested',
              'storage_temporary',
              'storage_resident',
              'storage_pbstore',
              'data_transfers'
              ),
          'description': help_text_supercomputer_job
          }
        ),


        ('', 
         {'fields': 
              (
              'LibraryInline',              
              ),
          'description': help_text_libraries
          }
        ),
       ('Review', 
          {'fields': 
               (
               'ReviewerScoreInline',              
               'ReviewerCommentInline',
               'hours_allocated',
               'ldap_project_name',
               ),
           'description': ''
           }
         ),
         ('Submit', 
          {'fields': 
               (
               'complete',              
               )
           }
         ),  
    ]

    def CSV_summary_of_LDAP_accounts(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        details = account_services.get_applications_CSV(selected)
        return HttpResponse("</br>".join(details))

    CSV_summary_of_LDAP_accounts.short_description = "Generate an LDAP account summary (CSV) for selected Applications."

    def create_ldap_groups(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        result = account_services.create_applications_groups(selected)
        message = "Created %s group(s) of the total of %s selected. Errors: %s" % (result['created'], len(selected), result['errors'])
        self.message_user(request, message)
        
    create_ldap_groups.short_description = "Create LDAP groups for selected application(s)"

    def queryset(self, request):

        # superuser - return all
        if request.user.is_superuser:
            return Application.objects.all()

        query_list = get_querylist(request=request)
    
        # reviewer - return all
        if query_list:
            return Application.objects.filter(reduce(operator.or_,query_list))

        # has change privilege - show them just their applications
        elif self.has_change_permission(request):
            return Application.objects.filter(created_by=request.user)

        # show none
        else:
            return Application.objects.none()


    
    def submitted(self, obj):
        return "Submitted" if obj.complete else "Not yet submitted"


    # add the user to created_by on save
    def save_model(self, request, obj, form, change):            
        if not change:
            obj.created_by = request.user
            
            # if the user is a director, force that priority area
            # (the option isn't on the form in this case)
            directors = Group.objects.get(name='directors')
            if directors in request.user.groups.all():
                obj.priority_area_directors = True
            
        obj.save()
    
    def add_view(self, request, form_url='', extra_context=None): 
        self.exclude_review_fields(request.user, ('allocation.add_reviewerscore', 'allocation.add_reviewercomment'))
        directors = Group.objects.get(name='directors')
        if directors in request.user.groups.all():            
            for i in self.fieldsets:
                if i[0] == 'Priority Areas':
                    self.fieldsets.remove(i)
                    self.exclude = ['priority_area_radio_astronomy',
                                    'priority_area_geosciences',
                                    'priority_area_directors',
                                    'priority_area_partner',
                                    'priority_area_national']
        return super(ApplicationAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)
    
    def change_view(self, request, object_id, extra_context=None):
        self.exclude_review_fields(request.user, ('allocation.change_reviewerscore', 'allocation.change_reviewercomment'))
        
        # do we let directors change the priority area on existing applications?
        # for now I'm guessing we do...
        # directors = Group.objects.get(name='directors')
        #         if directors in request.user.groups.all():            
        #             for i in self.fieldsets:
        #                 if i[0] == 'Priority Areas':
        #                     self.fieldsets.remove(i)
        #                     self.exclude = ['priority_area_radio_astronomy',
        #                                     'priority_area_geosciences',
        #                                     'priority_area_directors',
        #                                     'priority_area_partner',
        #                                     'priority_area_national']
                                    
        return super(ApplicationAdmin, self).change_view(request, object_id, extra_context=extra_context)
    
    # remove the entire Review fieldset (including the inlines) if permissions aren't met
    # necessary due to a known Django issue: https://code.djangoproject.com/ticket/8060
    def exclude_review_fields(self, user, permissions):
        restricted_inlines = [ReviewerScoreInline, ReviewerCommentInline] 
        inlines_to_remove = []
        for permission in permissions:
            if permission not in user.get_all_permissions():
                for i in self.inline_instances:
                    if i.__class__ in restricted_inlines:
                        inlines_to_remove.append(i)
                        self.inline_instances.remove(i)
                for i in self.fieldsets:
                    if i[0] == 'Review':
                        self.fieldsets.remove(i)
                self.exclude = ['hours_allocated', 'ldap_project_name']
                return
                
        # This instance is persistent between http requests.
        # If we didn't exclude the review fields on this request, then we may have done so previously.
        # If permissions have been changed in the meantime, we should actually do the opposite and add
        # these fields back in!
        for i in self.fieldsets:
            if i[0] == 'Review':
                return
        self.exclude = []
        self.fieldsets.insert(-1, ('Review', 
                                    {'fields': 
                                        (
                                        'ReviewerScoreInline',              
                                        'ReviewerCommentInline',
                                        'hours_allocated',
                                        'ldap_project_name',
                                        ),
                                    'description': ''
                                    }
                                  )
                             )
        self.inline_instances += [inline(self.model, self.admin_site) for inline in restricted_inlines]
        

class ParticipantAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'email', 'department_institute', 'application_id', 'status', 'account', 'has_account_details', 'fetched_from_ldap', 'hours_allocated', 'application_complete']
    # NOTE: the 'application__complete' filter depends on a patch of '/home/fjanon/ivecallocation/trunk/ivecallocation/django/contrib/admin/filterspecs.py'
    # See the note in that file
    list_filter = ['account', 'admin', 'student', 'status', 'range:application__hours_allocated', 'application__complete']
    #list_filter = ['account', 'admin', 'student', 'status', 'range:application__hours_allocated']
    search_fields = ['name', 'email']
    actions = ['fetch_ldap_details', 'send_account_creation_email', 'create_user_account', 'send_account_created_email', 'CSV_summary_of_LDAP_accounts']

    def fetch_ldap_details(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

        migrated_count = 0
        for id in selected:
            participant = Participant.objects.get(id=id)
            if account_services.fetch_old_ldap_details(participant):
                migrated_count += 1
            
        message = "Migrated details for %s participant(s) of the total of %s selected" % (migrated_count, len(selected))
        self.message_user(request, message)

    fetch_ldap_details.short_description = "Fetch account details from old LDAP."

    def send_account_creation_email(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

        for id in selected:
            participant = Participant.objects.get(id=id)
            account_services.send_account_creation_mail(participant, request)
            
        message = "Account creation email sent to %s participant(s)" % len(selected)
        self.message_user(request, message)

    send_account_creation_email.short_description = "Send account request creation email to selected Participants."

    def create_user_account(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        result = account_services.create_user_accounts(selected)
        created_count = result['created']
        updated_count = result['updated']
        error_count = result['errors']
        message = "Created %s account(s), updated %s of the total of %s selected. Errors: %s" % (created_count, updated_count, len(selected), error_count)
        self.message_user(request, message)
        
    create_user_account.short_description = "Create selected participant account(s) in LDAP"

    def send_account_created_email(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

        for id in selected:
            participant = Participant.objects.get(id=id)
            account_services.send_account_created_notification_mail(participant, request)
            
        message = "Account created notification email sent to %s participant(s)" % len(selected)
        self.message_user(request, message)

    send_account_created_email.short_description = "Send account created notification email to selected Participants."

    def CSV_summary_of_LDAP_accounts(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

        details = account_services.get_user_accounts_CSV(selected)
            
        return HttpResponse("</br>".join(details))

    CSV_summary_of_LDAP_accounts.short_description = "Generate an LDAP account summary (CSV) for selected Participants."

class ParticipantAccountAdminForm(forms.ModelForm):
    class Meta:
        model = ParticipantAccount

    def clean_uid(self):
        data = self.cleaned_data['uid']
        unique_uid = self.instance.get_unique_uid(test_uid=data)
        if data != unique_uid:
            raise forms.ValidationError('Non unique uid "%s": I suggest "%s".' % (data, unique_uid))
        return data

class ParticipantAccountAdmin(admin.ModelAdmin):
    form = ParticipantAccountAdminForm 


def register(site):
    site.register(Application, ApplicationAdmin)
##    site.register(ResearchClassification)
##    site.register(FieldOfResearchCode)
    site.register(Participant, ParticipantAdmin)
    site.register(ParticipantAccount, ParticipantAccountAdmin)
    site.register(Institution)
##    site.register(Publication)
##    site.register(ResearchFunding)
##    site.register(SupercomputerJob)
##    site.register(Library)
