from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
# Create your views here.

def employees(request):
  employee_list = Employee.objects.all()
  context = {'employee_list': employee_list}
  return render(request, 'Bangazon/employees.html', context)


def departments(request):
  department_list = Department.objects.all()
  context = {'department_list': department_list}
  return render(request, 'Bangazon/departments.html', context)

def computers(request):
  computer_list = Computer.objects.all()
  context = {'computer_list': computer_list}
  return render(request, 'Bangazon/computers.html', context)

def training_programs(request):
  training_program_list = TrainingProgram.objects.all()
  context = {'training_program_list': training_program_list}
  return render(request, 'Bangazon/training_program.html', context)