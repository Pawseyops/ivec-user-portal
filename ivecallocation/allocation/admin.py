# -*- coding: utf-8 -*-
from ivecallocation.allocation.models import *
from django.contrib import admin
from django import forms
from admin_forms import *

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
              ),
          }
        ),

        ('', 
         {'fields': 
              (
              'priority_area_radio_astronomy',
              'priority_area_geosciences',
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


def register(site):
    site.register(Application, ApplicationAdmin)
    site.register(ResearchClassification)
    site.register(FieldOfResearchCode)
    site.register(Participant)
    site.register(Publication)
    site.register(ResearchFunding)
    site.register(SupercomputerJob)
    site.register(Library)
