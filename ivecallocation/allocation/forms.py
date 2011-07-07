from django import forms 
from ivecallocation.allocation import models

class BaseParticipantAccountForm(forms.Form):
    first_name = forms.CharField(max_length=256 )
    last_name = forms.CharField(max_length=256)
    institution = forms.ModelChoiceField(queryset=models.Institution.objects.all()) 
    phone = forms.CharField(max_length=256, label='Phone number', required=False)

class ParticipantAccountForm(BaseParticipantAccountForm):
    tos = forms.BooleanField(widget=forms.CheckboxInput(),
                             label='I have read and agree to the Terms of Service',
                             error_messages={'required': "You must agree to the terms to register"      })

class ParticipantAccountWithPasswordForm(BaseParticipantAccountForm):
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Password (again)')
    tos = forms.BooleanField(widget=forms.CheckboxInput(),
                             label='I have read and agree to the Terms of Service',
                             error_messages={'required': "You must agree to the terms to register"      })

   
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("The two password fields didn't match.")
        return self.cleaned_data

