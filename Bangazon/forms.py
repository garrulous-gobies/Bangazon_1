from django import forms
from django.utils import timezone

class NewTrainingForm(forms.Form):
    training_name = forms.CharField(label='Training Title', max_length=100, required=True)
    training_description = forms.CharField(label='Training Description', max_length=250, required=True)
    training_startDate = forms.DateTimeField(initial=timezone.now(), required=True)
    training_endDate = forms.DateTimeField(initial=timezone.now(), required=True)
    training_maxEnrollment = forms.IntegerField(label='Max Class Size', required=True)
