# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as DjangoUser

#from choices import *
from help_text import *


# TODO setup logging
#import logging
#logger = logging.getLogger('ivecallocation')

class Application(models.Model):
    project_title = models.CharField(max_length=100, help_text=help_text_project_title, null=True, blank=True)
    project_summary = models.CharField(max_length=1000, help_text=help_text_project_summary, null=True, blank=True)
    priority_area_radio_astronomy = models.BooleanField(help_text=help_text_priority_areas)
    priority_area_geosciences = models.BooleanField(help_text=help_text_priority_areas)
    research_record = models.CharField(max_length=5000, help_text=help_text_research_record, null=True, blank=True)
    research_significance = models.CharField(max_length=5000, null=True, blank=True)
    computational_methodology = models.CharField(max_length=5000, null=True, blank=True)
    core_hours_requested = models.IntegerField(null=True, blank=True)
    storage_temporary = models.FloatField(null=True, blank=True)
    storage_resident = models.FloatField(null=True, blank=True)
    storage_pbstore = models.FloatField(null=True, blank=True)
    data_transfers = models.CharField(max_length=512, null=True, blank=True)
    created_by = models.ForeignKey(DjangoUser, editable=False, related_name="%(class)s_creators",null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    complete =  models.BooleanField(verbose_name="ready to submit application")

    def __unicode__(self):
        return "%s" % self.project_title


class ResearchClassification(models.Model):
    application = models.ForeignKey(Application)
    code = models.IntegerField(null=True, blank=True)
    percentage = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.code


class FieldOfResearchCode(models.Model):
    code = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.code


class Participant(models.Model):
    application = models.ForeignKey(Application)
    name = models.CharField(max_length=256, null=True, blank=True)
    department_institute = models.CharField(max_length=128, verbose_name="Department, Institute", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    account = models.BooleanField()
    admin = models.BooleanField()
    student = models.BooleanField()
    eft = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.name

    
class Publication(models.Model):
    application = models.ForeignKey(Application)
    reference = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.reference


class ResearchFunding(models.Model):
    application = models.ForeignKey(Application)    
    participant = models.CharField(max_length=256, null=True, blank=True)
    funding_source = models.CharField(max_length=256, help_text="Include grant ID number if applicable", null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    total_funding = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "research funding"
        verbose_name_plural = "research funding"

    def __unicode__(self):
        return "%s" % self.participant


class SupportingFunding(models.Model):
    application = models.ForeignKey(Application)    
    participant = models.CharField(max_length=256, null=True, blank=True)
    funding_source = models.CharField(max_length=256, help_text="Include grant ID number if applicable", null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    years = models.IntegerField(null=True, blank=True)
    total_funding = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "supporting funding"
        verbose_name_plural = "supporting funding"

    def __unicode__(self):
        return "%s" % self.participant


class SupercomputerJob(models.Model):
    JOB_TYPE_CHOICES = (
        ("l", "Largest"),
        ("t", "Typical"),
        ("s", "Smallest"),
        )

    application = models.ForeignKey(Application)
    job_type = models.CharField(max_length=1, choices=JOB_TYPE_CHOICES, null=True, blank=True)
    processes = models.IntegerField(verbose_name="Number of (MPI) processes", null=True, blank=True)
    processes_per_node = models.IntegerField(null=True, blank=True)
    wallclock_time_per_job = models.IntegerField(null=True, blank=True)
    number_of_type_of_job = models.IntegerField(verbose_name="Number of jobs of this type", null=True, blank=True)
    total_memory = models.IntegerField(null=True, blank=True)
    data_transfer = models.IntegerField(verbose_name="Amount of data read/written to disk", null=True, blank=True)



class Library(models.Model):
    application = models.ForeignKey(Application)
    description = models.CharField(max_length=256, null=True, blank=True)
    reference = models.CharField(max_length=256, null=True, blank=True)
    licensing = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "application, tool or library"
        verbose_name_plural = "applications, tools or libraries"
    
    def __unicode__(self):
        return "%s" % self.description
