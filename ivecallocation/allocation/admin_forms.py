from django import forms
from django.contrib.auth.models import User, Group
from models import *
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm
from ccg.recaptcha import *

class SystemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SystemForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget = forms.TextInput(attrs={'size':'100'})
    class Meta:
        model = System

class AllocationRoundForm(forms.ModelForm):
    class Meta:
        model = AllocationRound

class ApplicationForm(forms.ModelForm):      
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields["project_title"].widget = forms.TextInput(attrs={'size':'100'})
        self.fields["project_summary"].widget = forms.Textarea(attrs={'rows':16, 'cols':120})
        self.fields["research_record"].widget = forms.Textarea(attrs={'rows':16, 'cols':120})
        self.fields["research_significance"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})
        self.fields["computational_methodology"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})
        self.fields["data_transfers"].widget = forms.Textarea(attrs={'rows':6, 'cols':100}) #field is 512 chars max in model
        
        now = datetime.now()
        
        self.fields["allocation_round"].empty_label = "-- select allocation round --"
        self.fields["priority_area"].empty_label = "-- select priority area --"
        
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields["allocation_round"].queryset = AllocationRound.objects.filter(
                Q(start_date__lte=now, end_date__gte=now) | Q(id=instance.allocation_round.id))
            self.fields['allocation_round'].widget.widget.attrs['disabled'] = True
            self.fields['allocation_round'].widget.attrs['readonly'] = True
            self.fields["priority_area"].queryset = PriorityArea.objects.filter(allocationround=instance.allocation_round)
        else:
            self.fields["allocation_round"].queryset = AllocationRound.objects.filter(
                start_date__lte=now, end_date__gte=now)
            self.fields["allocation_round"].widget.widget = forms.Select(attrs={})
            
        directors = Group.objects.get(name='directors')
        if directors in self.request.user.groups.all():
            self.director_form = True
            self.fields["priority_area"].queryset = PriorityArea.objects.filter(code='director')
            self.fields['priority_area'].initial = PriorityArea.objects.get(code='director')
            self.fields['priority_area'].widget.widget.attrs['disabled'] = True
            self.fields['priority_area'].widget.attrs['readonly'] = True
 
    def clean(self):   
        # Allocation round is expected to be absent on change...
        instance = getattr(self, 'instance', None)
        if instance and instance.id and 'allocation_round' in self._errors:
            del self._errors['allocation_round']
            self.cleaned_data['allocation_round'] = self.instance.allocation_round
        
        # priority area must be among those valid for the allocation round          
        allocation_round = self.cleaned_data.get("allocation_round")
        if self.director_form:
            priority_area = PriorityArea.objects.get(code='director')
        else:
            priority_area = self.cleaned_data.get("priority_area")
        if allocation_round and priority_area not in allocation_round.priority_area.all():
            error = "Priority area %s is not available for allocation round %s" % (priority_area, allocation_round)
            self._errors["priority_area"] = self.error_class([error])
            
        return self.cleaned_data
    
    def clean_allocation_round(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return self.instance.allocation_round
        else:
            return self.cleaned_data['allocation_round']
    
    class Meta:
        model = Application


class RestrictedApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RestrictedApplicationForm, self).__init__(*args, **kwargs)
        assert False
        self.fields["project_title"].widget = forms.TextInput(attrs={'size':'10'})
        self.fields["project_summary"].widget = forms.Textarea(attrs={'rows':16, 'cols':120})
        self.fields["research_record"].widget = forms.Textarea(attrs={'rows':16, 'cols':120})
        self.fields["research_significance"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})
        self.fields["computational_methodology"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})

        self.fields["data_transfers"].widget = forms.Textarea(attrs={'rows':6, 'cols':100}) #field is 512 chars max in model


    class Meta:
        model = Application



class PublicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.fields["reference"].widget = forms.Textarea(attrs={'rows':4, 'cols':80}) # field is 256 chars max in model
        self.fields["description"].widget = forms.Textarea(attrs={'rows':4, 'cols':80}) # verbose name: 'significance', field is 256 chars max in model

    class Meta:
        model = Publication

class ReviewerScoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewerScoreForm, self).__init__(*args, **kwargs)

    reviewer = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), required=True)

    class Meta:
        model = ReviewerScore


class ReviewerCommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewerCommentForm, self).__init__(*args, **kwargs)

    reviewer = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), required=True)

    class Meta:
        model = ReviewerComment


class RecaptchaPasswordResetForm(RecaptchaForm, PasswordResetForm):
    
    captcha = RecaptchaFieldPlaceholder(widget=RecaptchaWidget(theme='white'),
                                        label='Are you a human?')
    
    def __init__(self, remote_ip=None, *args):
        print "Called init"
        if remote_ip:
            self.remote_ip = remote_ip
        return super(RecaptchaPasswordResetForm, self).__init__(self.remote_ip, *args)
        
    def __call__(self, *args):
        return RecaptchaPasswordResetForm(self.remote_ip, *args)

