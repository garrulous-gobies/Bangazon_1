from django.shortcuts import render,  get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import *
# Create your views here.

def employees(request):
  employee_list = Employee.objects.all()
  context = {'employee_list': employee_list}
  return render(request, 'Bangazon/employees.html', context)

# 
def departments(request):
  # department_list = get_list_or_404(Department, )
  department_list = Department.objects.all()
  employee_list = Employee.objects.all()
  context = {'department_list': department_list, 'employee_list': employee_list}
  return render(request, 'Bangazon/departments.html', context)

def computers(request):
  computer_list = Computer.objects.all()
  context = {'computer_list': computer_list}
  return render(request, 'Bangazon/computers.html', context)

def training_programs(request):
  now = timezone.now()
  print("Date: ", now)
  training_program_list = TrainingProgram.objects.filter(startDate__gte=now)
  context = {'training_program_list': training_program_list}
  return render(request, 'Bangazon/training_program.html', context)

def past_training_programs(request):
  now = timezone.now()
  print("Date: ", now)
  training_program_list = TrainingProgram.objects.filter(startDate__lte=now)
  context = {'training_program_list': training_program_list}
  return render(request, 'Bangazon/past_training_programs.html', context)

def training_details(request, pk):
  training_program_details = get_object_or_404(TrainingProgram, id = pk)
  context = {'training_program_details': training_program_details}
  return render(request, 'Bangazon/indiv_training_program.html', context)
