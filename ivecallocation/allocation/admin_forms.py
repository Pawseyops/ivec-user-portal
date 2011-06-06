from django import forms
from models import *

class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields["project_title"].widget = forms.TextInput(attrs={'size':'100'})
        self.fields["project_summary"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})
        self.fields["research_record"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})
        self.fields["research_significance"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})
        self.fields["computational_methodology"].widget = forms.Textarea(attrs={'rows':16, 'cols':100})

        self.fields["data_transfers"].widget = forms.Textarea(attrs={'rows':6, 'cols':100}) #field is 512 chars max in model
        self.fields["reference"].widget = forms.Textarea(attrs={'rows':3, 'cols':100}) #field is 256 chars max in model
        self.fields["description"].widget = forms.Textarea(attrs={'rows':3, 'cols':100}) # verbose name: 'significance', field is 256 chars max in model

    class Meta:
        model = Application
