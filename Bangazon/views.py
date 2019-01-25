from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
# Create your views here.

def employees(request):
  employee_list = Employee.objects.all()
  context = {'employee_list': employee_list}
  return render(request, 'Bangazon/employees.html', context)