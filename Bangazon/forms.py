from django import forms
from datetime import datetime

class NewTrainingForm(forms.Form):
    training_name = forms.CharField(label='Training Title', max_length=100, required=True)
    training_description = forms.CharField(label='Training Description', max_length=250, required=True)
    training_startDate = forms.DateTimeField(initial=datetime.now(), required=True)
    training_endDate = forms.DateTimeField(initial=datetime.now(), required=True)
    training_maxEnrollment = forms.IntegerField(initial= 10, min_value=1, max_value=100 ,label='Max Class Size', required=True)
