from django import forms
from datetime import datetime
from .models import *

departments = Department.objects.all()

dept_list = list()
for department in departments:
    dept = ('department', department.name)
    dept_list.append(dept)

department_list = tuple(dept_list)



class EmployeeEditForm(forms.Form):
    
    firstName = forms.CharField(label='First Name', max_length=35, required=True)
    lastName = forms.CharField(label='Last Name', max_length=35, required=True)
    startDate = forms.DateTimeField(initial=datetime.now(), required=True, label='Start Date')
    isSupervisor = forms.ChoiceField(label='Supervisor', choices=((0, 'No'), (1, 'Yes')))
    departments = forms.ChoiceField(label='Department', choices=(department_list))