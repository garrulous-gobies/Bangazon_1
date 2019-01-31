from django import forms
from datetime import datetime
from .models import *


class EmployeeEditForm(forms.Form):
<<<<<<< HEAD
    def __init__(self, **kwargs):
        self.department_choices = kwargs.pop('dept_choices')
        # self.computer_choices = kwargs.pop('comp_choices')
        # self.training_choices = kwargs.pop('train_choices')
        super(EmployeeEditForm, self).__init__(**kwargs)
        self.fields['department'] = forms.ChoiceField(label='Department', choices=(self.department_choices))
        # self.fields['computer'] = forms.ChoiceField(label='Computer', choices = self.computer_choices)
        # self.fields['training'] = forms.Select(label="Training Enrollment", choices = self.training_choices)

=======
>>>>>>> master
    firstName = forms.CharField(label='First Name', max_length=35, required=True)
    lastName = forms.CharField(label='Last Name', max_length=35, required=True)
    startDate = forms.DateTimeField(initial=datetime.now(), required=True, label='Start Date')
    supervisor = forms.ChoiceField(label='Supervisor', choices=((0, 'No'), (1, 'Yes')))


class NewTrainingForm(forms.Form):
    training_name = forms.CharField(label='Training Title', max_length=100, required=True)
    training_description = forms.CharField(label='Training Description', max_length=250, required=True)
    training_startDate = forms.DateTimeField(initial=datetime.now(), required=True)
    training_endDate = forms.DateTimeField(initial=datetime.now(), required=True)
    training_maxEnrollment = forms.IntegerField(initial= 10, min_value=1, max_value=100 ,label='Max Class Size', required=True)
