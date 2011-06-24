from django import forms
from django.contrib.auth.models import User
from models import *

class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields["project_title"].widget = forms.TextInput(attrs={'size':'100'})
        self.fields["project_summary"].widget = forms.Textarea(attrs={'rows':16, 'cols':120})
        self.fields["research_record"].widget = forms.Textarea(attrs={'rows':16, 'cols':120})
        self.fields["research_significance"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})
        self.fields["computational_methodology"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})

        self.fields["data_transfers"].widget = forms.Textarea(attrs={'rows':6, 'cols':100}) #field is 512 chars max in model

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




