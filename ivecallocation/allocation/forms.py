from django.forms import ModelForm
from ivecallocation.allocation import models

class ParticipantAccountForm(ModelForm):
    class Meta:
        model = models.ParticipantAccount
        fields = ['first_name', 'last_name', 'phone']

