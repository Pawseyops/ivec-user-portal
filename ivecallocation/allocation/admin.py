# -*- coding: utf-8 -*-
from ivecallocation.allocation.models import *
from django.contrib import admin
from django import forms
from admin_forms import *

class ResearchClassificationInline(admin.TabularInline):
    model = ResearchClassification
    extra = 3

class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 4

class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 10

class ResearchFundingInline(admin.TabularInline):
    model = ResearchFunding
    extra = 10

class SupportingFundingInline(admin.TabularInline):
    model = SupportingFunding
    extra = 10    

class SupercomputerJobInline(admin.TabularInline):
    model = SupercomputerJob
    extra = 3

class LibraryInline(admin.TabularInline):
    model = Library
    extra = 5

class ApplicationAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['project_title', 'submitted']
    inlines = [ResearchClassificationInline, ParticipantInline, PublicationInline, ResearchFundingInline, SupportingFundingInline, SupercomputerJobInline, LibraryInline ] 
    form = ApplicationForm
    
    fieldsets = (
        ('Part A - Summary', 
         {'fields': 
              (
              'project_title',
              'project_summary',
              'priority_area_radio_astronomy',
              'priority_area_geosciences',
              ),
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
          'description':'Here is my text Here is my text Here is<br/> my text Here is my text Here is my text Here is my text '
          }
        ),




        ('Part B - Project Team', 
         {'fields': 
              (
              'research_record',
              'PublicationInline',
              'ResearchFundingInline'
              
              )
          }
        ),
        ('Part C - Research Proposal', 
         {'fields': 
              (
              'research_significance',
              'computational_methodology',
              'SupportingFundingInline'
              
              )
          }
        ),
        ('Part D - Resource Request', 
         {'fields': 
              (
              'SupercomputerJobInline',
              'core_hours_requested',
              'LibraryInline',
              'storage_temporary',
              'storage_resident',
              'storage_pbstore',
              'data_transfers'
              
              )
          }
        ),
        ('Submit', 
         {'fields': 
              (
              'complete',              
              )
          }
        ),        

    )

    def queryset(self, request):

        if request.user.is_superuser:
            return Application.objects.all()

        if self.has_change_permission(request):
            return Application.objects.filter(created_by=request.user)
        else:
            return Application.objects.none()

    # add the user to created_by on save
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()

    def submitted(self, obj):
        return "Submitted" if obj.complete else "Not yet submitted"

admin.site.register(Application, ApplicationAdmin)
admin.site.register(ResearchClassification)
admin.site.register(FieldOfResearchCode)
admin.site.register(Participant)
admin.site.register(Publication)
admin.site.register(ResearchFunding)
admin.site.register(SupercomputerJob)
admin.site.register(Library)



