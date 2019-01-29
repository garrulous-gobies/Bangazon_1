from django.shortcuts import render,  get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import *

# ======================== EMPLOYEES ================
def employees(request):
  employee_list = Employee.objects.all()
  context = {'employee_list': employee_list}
  return render(request, 'Bangazon/employees.html', context)

def employee_details(request, employee_id):
    now = timezone.now()
    employee_details = Employee.objects.get(pk=employee_id)
    past_training_programs = list()
    upcoming_training_programs = list()
    for program in employee_details.trainingprogram_set.all():
        if (program.startDate < now):
            past_training_programs.append(program)
        elif (program.startDate > now):
            upcoming_training_programs.append(program)
    context = {
        'employee_details': employee_details,
        'past_training_programs':past_training_programs,
        'upcoming_training_programs': upcoming_training_programs
        }
    return render(request, 'Bangazon/employee_details.html', context)

def employee_form(request):
    departments = Department.objects.all()
    context = {"departments": departments}
    return render(request, "Bangazon/employees_form.html", context)

def employee_new(request):
    department = Department.objects.get(pk=request.POST['department'])
    employee = Employee(firstName = request.POST['firstName'], lastName = request.POST['lastName'], startDate = request.POST['startDate'], isSupervisor = request.POST['supervisor'], department = department)

    employee.save()
    return HttpResponseRedirect(reverse('Bangazon:employees'))

# ========================DEPARTMENTS================
def departments(request):
    department_list = Department.objects.all()
    context = {'department_list': department_list}
    return render(request, 'Bangazon/departments.html', context)

def new_department(request):
    department_list = Department.objects.all()
    context = {'department_list': department_list}
    return render(request, 'Bangazon/new_department_form.html', context)

def save_department(request):
    name = request.POST['department_name']
    budget = request.POST['department_budget']
    dep = Department(name=name, budget=budget)
    dep.save()
    return HttpResponseRedirect(reverse('Bangazon:departments'))

def department_details(request, department_id):
    department_details = Department.objects.get(pk=department_id)
    context = {'department_details': department_details}
    return render(request, 'Bangazon/department_details.html', context)

# ==========================COMPUTERS=================================
def computers(request):
    computer_list = Computer.objects.all()
    context = {'computer_list': computer_list}
    return render(request, 'Bangazon/computers.html', context)

def computer_details(request, computer_id):
  computer = get_object_or_404(Computer, pk=computer_id)
  print("id", computer.id)
  context = {'computer': computer}
  return render(request, 'Bangazon/computer_details.html', context)

def computer_form(request):
    employees = Employee.objects.all
    context = {"employees": employees}
    return render(request, "Bangazon/computer_form.html", context)

def computer_new(request):
    computer = Computer(purchaseDate = request.POST['purchase'], model= request.POST['model'], manufacturer = request.POST['manufacturer'])
    computer.save()
    employee = Employee.objects.get(pk=request.POST['assignment'])
    relationship = Employee_Computer(employee=employee, computer=computer)
    relationship.save()
    return HttpResponseRedirect(reverse('Bangazon:computers'))

def computer_delete_confirm(request):
    computer= Computer.objects.get(pk=request.POST['computer_id'])
    is_assigned=computer.employee_set.all()
    assigned = False
    if len(is_assigned) > 0:
        assigned = True
    context = {'computer': computer,
                'assigned': assigned}
    print("context", context)
    return render(request, "Bangazon/computer_delete_confirm.html", context)

def computer_delete(request):
    computer= Computer.objects.get(pk=request.POST['computer_id'])
    computer.delete()
    return HttpResponseRedirect(reverse('Bangazon:computers'))




# =====================================================================

def training_programs(request):
  now = timezone.now()
  training_program_list = TrainingProgram.objects.filter(startDate__gte=now)
  context = {'training_program_list': training_program_list}
  return render(request, 'Bangazon/training_program.html', context)

def past_training_programs(request):
  now = timezone.now()
  training_program_list = TrainingProgram.objects.filter(startDate__lte=now)
  context = {'training_program_list': training_program_list}
  return render(request, 'Bangazon/past_training_programs.html', context)

def new_training_program_form(request):
  return render(request, 'Bangazon/new_training_program_form.html')

def save_program(request):
  name = request.POST['training_name']
  description = request.POST['training_description']
  startDate= request.POST['training_startDate']
  endDate = request.POST['training_endDate']
  maxEnrollment = request.POST['training_maxEnrollment']
  t = TrainingProgram(name = name, description = description, startDate = startDate, endDate = endDate, maxEnrollment = maxEnrollment)
  t.save()
  response = redirect('./Training')
  return response

def training_details(request, pk):
  training_program_details = get_object_or_404(TrainingProgram, id = pk)
  training_attendees = EmployeeTrainingProgram.objects.filter(trainingProgram_id = pk)
  all_attendees = []
  for user in training_attendees:
    employee_trained = get_object_or_404(Employee, id = user.employee_id)
    all_attendees.append(employee_trained)
  context = {'training_program_details': training_program_details, 'all_attendees': all_attendees}
  return render(request, 'Bangazon/indiv_training_program.html', context)