# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.db.models import Avg
from django.core.urlresolvers import reverse

#from choices import *
from help_text import *


# TODO setup logging
#import logging
#logger = logging.getLogger('ivecallocation')

class Application(models.Model):
    project_title = models.CharField(max_length=100, help_text=help_text_project_title)
    project_summary = models.CharField(max_length=1000, help_text=help_text_project_summary, null=True, blank=True)
    priority_area_radio_astronomy = models.BooleanField()
    priority_area_geosciences = models.BooleanField()
    priority_area_directors = models.BooleanField()
    priority_area_partner = models.BooleanField()
    priority_area_national = models.BooleanField()    
    research_record = models.CharField(max_length=5000, help_text=help_text_research_record, null=True, blank=True)
    research_significance = models.CharField(max_length=5000, help_text=help_text_research_significance, null=True, blank=True)
    computational_methodology = models.CharField(max_length=5000, help_text=help_text_computational_methodology, null=True, blank=True)
    core_hours_requested = models.IntegerField(null=True, blank=True, help_text=help_text_core_hours)
    hours_allocated = models.IntegerField(null=True, blank=True)    
    storage_temporary = models.CharField(max_length=32, null=True, blank=True, help_text=help_text_storage_temporary)
    storage_resident = models.CharField(max_length=32, null=True, blank=True, help_text=help_text_storage_resident)
    storage_pbstore = models.CharField(max_length=32, null=True, blank=True, help_text=help_text_storage_pbstore)
    data_transfers = models.CharField(max_length=512, null=True, blank=True, help_text=help_text_data_transfers)
    ldap_project_name = models.CharField(max_length=256, null=True, blank=True)
    created_by = models.ForeignKey(DjangoUser, editable=False, related_name="%(class)s_creators",null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    complete =  models.BooleanField(verbose_name="ready to submit application")

    def __cmp__(self, other):
        if self.overall_score() < other.overall_score():
            return 1
        elif self.overall_score() > other.overall_score():
            return -1
        else:
            return 0

    def __unicode__(self):
        return "%s" % self.project_title


    def overall_score(self):
        # aggregate returns dictionary, so just return the value
        return self.reviewerscore_set.all().aggregate(Avg('score')).get('score__avg', None)

    def reviews(self):
        return self.reviewerscore_set.all().count()        

    @property
    def priority_area(self):
        if self.priority_area_radio_astronomy:
            return 'Radio Astronomy'
        elif self.priority_area_geosciences:
            return 'Geosciences'
        elif self.priority_area_directors:
            return 'Directors'
        elif self.priority_area_partner:
            return 'Partner'
        elif self.priority_area_national:
            return 'National'
        else:
            return None




class ReviewerScore(models.Model):
    application = models.ForeignKey(Application)    
    research_merit = models.IntegerField(null=True, blank=True)
    computational_merit = models.IntegerField(null=True, blank=True)    
    score = models.IntegerField(null=True, blank=True)
    reviewer = models.ForeignKey(DjangoUser, related_name="%(class)s_reviewers", null=True)

    def save(self, *args, **kwargs):
        self.score = min(self.research_merit, self.computational_merit)
        super(ReviewerScore, self).save(*args, **kwargs) # Call the "real" save() method.

class ReviewerComment(models.Model):
    application = models.ForeignKey(Application)    
    reviewer_comment = models.TextField(null=True, blank=True)
    reviewer = models.ForeignKey(DjangoUser, related_name="%(class)s_reviewers", null=True)    

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

class ParticipantStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "%s" % self.name

class Participant(models.Model):
    STATUS = {
        'NEW': 1,
        'EMAIL_SENT': 2,
        'DETAILS_FILLED': 3,
        'ACCOUNT_CREATED': 4,
        'ACCOUNT_CREATED_EMAIL_SENT': 5,
    }

    application = models.ForeignKey(Application)
    name = models.CharField(max_length=256, null=True, blank=True)
    department_institute = models.CharField(max_length=128, verbose_name="Department, Institution", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    account = models.BooleanField()
    admin = models.BooleanField()
    student = models.BooleanField()
    eft = models.FloatField(null=True, blank=True, verbose_name="EFT %")
    status = models.ForeignKey(ParticipantStatus)
    account_email_hash = models.CharField(max_length=50, null=True, blank=True) 
    account_email_on = models.DateTimeField(null=True, blank=True)
    details_filled_on = models.DateTimeField(null=True, blank=True)
    account_created_on = models.DateTimeField(null=True, blank=True)
    account_created_email_on = models.DateTimeField(null=True, blank=True)

    def has_account_details(self):
        try:
            self.participantaccount
            # TODO why doesn't this work? works for participant, not for participantaccount
            #url = reverse('admin:allocation_participantaccount_change', args=[self.participant.id] )
            url = '../participantaccount/%s' % self.participantaccount.id 
            return "<a href='%s'>Yes</a>" % url
        except ParticipantAccount.DoesNotExist:
            return 'No'
    has_account_details.allow_tags = True

    def fetched_from_ldap(self):
        try:
            pa = self.participantaccount
            return pa.data_fetched_on is not None
        except ParticipantAccount.DoesNotExist:
            return False

    def application_id(self):
        return self.application_id
    application_id.admin_order_field = 'application__id'

    def hours_allocated(self):
        return self.application.hours_allocated
    hours_allocated.admin_order_field = 'application__hours_allocated'

    def __unicode__(self):
        return "%s" % self.name

class Institution(models.Model):
    display_name = models.CharField(max_length=256, null=False, blank=False)
    ldap_ou_name = models.CharField(max_length=256, null=False, blank=False)

    def __unicode__(self):
        return "%s" % self.display_name

class ParticipantAccount(models.Model):
    participant = models.OneToOneField(Participant)
    institution = models.ForeignKey(Institution, null=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    phone = models.CharField(max_length=50, null=True, blank=True)
    uid = models.CharField(max_length=256, null=True, blank=True)
    uid_number = models.IntegerField(null=True, blank=True)
    gid_number = models.IntegerField(null=True, blank=True)
    password_hash = models.CharField(('password'), max_length=256, null=True, blank=True)

    old_ldap_details = models.CharField(max_length=2000, null=True, blank=True)
    data_fetched_on = models.DateTimeField(null=True, blank=True)
    
    def get_unique_uid(self):
        
        def check_unique_uid(uid):
            qs = ParticipantAccount.objects.filter(uid = uid)
            if len(qs) > 1:
                return False
            else:
                return True
        
        #Check to see if we have the same uid as anyone else.
        #if so, try for a uid using firstname + lastname[0]
        #and if that still conflicts, use self.uid + 1,2,3 etc
        original_uid = self.uid
        
        if original_uid is None or len(original_uid) == 0:
           original_uid = self.first_name.lower()

        #catch uid's that have somehow come with a capitalisation.
        if original_uid.lower() != original_uid:
            original_uid = original_uid.lower()

        candidate_uid = original_uid 
        if not check_unique_uid(candidate_uid):
            candidate_uid = ("%s%s" % (self.first_name, self.last_name[0])).lower()
            counter = 1
            while not check_unique_uid(candidate_uid):
                candidate_uid = ("%s%s" % (original_uid, str(counter))).lower()
                counter +=1

        return candidate_uid

    def constrain_uidgid(self):
        '''Ensures the users uidnumber and gidnumber are over 20k, and unique in the database.
           Can only be called after the user has already been saved.
        '''
        offset = 20050
        if ( (self.uid_number != self.id + offset) or (self.gid_number != self.id+offset)):
            self.uid_number = self.id + offset
            self.gid_number = self.id + offset
            self.save()

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Publication(models.Model):
    application = models.ForeignKey(Application)
    reference = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=256, null=True, blank=True, verbose_name="significance")

    def __unicode__(self):
        return "%s" % self.reference


class ResearchFunding(models.Model):
    application = models.ForeignKey(Application)    
    participant = models.CharField(max_length=256, null=True, blank=True)
    funding_source = models.CharField(max_length=256, help_text="Include grant ID number if applicable", null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    years = models.CharField(max_length=64, null=True, blank=True)
    total_funding = models.CharField(max_length=64, null=True, blank=True)

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
    years = models.CharField(max_length=64, null=True, blank=True)
    total_funding = models.CharField(max_length=64, null=True, blank=True)

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
    wallclock_time_per_job = models.CharField(max_length=32, null=True, blank=True)
    number_of_type_of_job = models.IntegerField(verbose_name="Number of jobs of this type", null=True, blank=True)
    total_memory = models.CharField(max_length=32, null=True, blank=True)
    data_transfer = models.CharField(max_length=32, verbose_name="Amount of data read/written to disk", null=True, blank=True)



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


