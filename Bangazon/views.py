from django.shortcuts import render,  get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import *
import math
from .forms import *
import datetime
import pytz
from django.db.models import Q


# ======================== Landing Page ================
def landing_page(request):
    return render(request, 'Bangazon/main.html')


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
        'past_training_programs': past_training_programs,
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

def employee_update(request, pk):
    department = Department.objects.get(pk=request.POST['department'])
    employee_edited = Employee(id=pk, firstName = request.POST['firstName'], lastName = request.POST['lastName'], startDate = request.POST['startDate'], isSupervisor = request.POST['supervisor'], department = department)

    employee_edited.save()
    return HttpResponseRedirect(reverse('Bangazon:employees'))

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    now = timezone.now()




    all_computers = Computer.objects.filter(decommissionDate = None)
    comp_relationships = Employee_Computer.objects.filter(removeDate= None)
    comp_list = list()
    # appends to comp_list only computers that are currently in commission and are not assigned to an employee
    for unassigned_comp in comp_relationships:
        for computer in all_computers:
            if unassigned_comp.id == computer.id:
                comp_list.append((computer.id, f'{computer.manufacturer} {computer.model}'))
    # inserts the employees currently assigned employee to the dropdown
    if len(employee.computer.all()) > 0:
        current_computer = employee.computer.all()[0]
        comp_list.insert(0, (current_computer.id, f'{current_computer.manufacturer} {current_computer.model}'))
        initial_comp_id = current_computer.id
    else:
        initial_comp_id = 0


    comp_list.insert(0, (0, 'None Assigned'))


    dept_list = list()
    departments = Department.objects.all()
    for department in departments:
        dept = (department.id, department.name)
        dept_list.append(dept)

    train_list = list()
    training_program_list = TrainingProgram.objects.filter(startDate__gte=now)
    for program in training_program_list:
        train_list.append((program.id, f'{program.name}-beginning:{program.startDate}'))


    current_enrollment = list()
    for program in employee.trainingprogram_set.all():
        current_enrollment.append(program.id)


    # convert list of choice tuples into a tuple for passing to form class
    computer_list = tuple(comp_list)
    department_list = tuple(dept_list)
    training_list = tuple(train_list)

    department = Department.objects.get(employee=pk)
    form = EmployeeEditForm(dept_choices = department_list,
                            comp_choices = computer_list,
                            train_choices = training_list,
                            initial={
                                'firstName': employee.firstName,
                                'lastName': employee.lastName,
                                'Start Date': employee.startDate,
                                'supervisor': employee.isSupervisor,
                                'department': department.id,
                                'computer': initial_comp_id,
                                'training': current_enrollment
                                }
                            )
    return render(request, 'Bangazon/employee_edit.html', {'form': form, 'employee': employee})

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
    if request.POST:
        computer_list = Computer.objects.filter(Q(manufacturer__icontains=request.POST['computer_search']) | Q(model__icontains=request.POST['computer_search']))
    else:
        computer_list = Computer.objects.all()

    context = {'computer_list': computer_list}
    return render(request, 'Bangazon/computer1.html', context)


def computer_details(request, computer_id):
  computer = get_object_or_404(Computer, pk=computer_id)
  context = {'computer': computer}
  return render(request, 'Bangazon/computer_details.html', context)

def computer_form(request):
    employees = Employee.objects.all()
    employee_computer = Employee_Computer.objects.all()
    employee_computer_have_computer = list()
    for rel in employee_computer:
        if rel.removeDate == None:
            employee_computer_have_computer.append(rel.employee_id)
    employee_filterd_list = list()
    for employee in employees:
        if employee.id not in employee_computer_have_computer:
            employee_filterd_list.append(employee)
    context = {"employees": employee_filterd_list}
    return render(request, "Bangazon/computer_form.html", context)


def computer_new(request):
    computer = Computer(
        purchaseDate=request.POST['purchase'], model=request.POST['model'], manufacturer=request.POST['manufacturer'])
    computer.save()
    if request.POST['assignment'] != 'null':
        employee = Employee.objects.get(pk=request.POST['assignment'])
        relationship = Employee_Computer(employee=employee, computer=computer, assignDate=datetime.datetime.now())
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
    return render(request, "Bangazon/computer_delete_confirm.html", context)

def computer_delete(request):
    computer= Computer.objects.get(pk=request.POST['computer_id'])
    computer.delete()
    return HttpResponseRedirect(reverse('Bangazon:computers'))

# ===========================TRAINING================================

# Lists all training programs for future classes
def training_programs(request):
    now = timezone.now()
    training_program_list = TrainingProgram.objects.filter(startDate__gte=now)
    context = {'training_program_list': training_program_list}
    return render(request, 'Bangazon/training_program.html', context)

# List past training programs that have taken place
def past_training_programs(request):
    now = timezone.now()
    training_program_list = TrainingProgram.objects.filter(startDate__lte=now)
    context = {'training_program_list': training_program_list}
    return render(request, 'Bangazon/past_training_programs.html', context)

# Show specific details for upcoming training classes with options to edit or delete
def training_details(request, trainingprogram_id):
    training_program_details = get_object_or_404(TrainingProgram, id=trainingprogram_id)
    assignees = EmployeeTrainingProgram.objects.filter(trainingProgram_id=training_program_details.id)
    attendees = []
    for emp in assignees:
        person = Employee.objects.get(id=emp.id)
        attendees.append(person)
    context = {'training_program_details': training_program_details, 'attendees': attendees}
    return render(request, 'Bangazon/indiv_training_program.html', context)

# Show specific details for past training classes without the option to alter data
def past_training_details(request, trainingprogram_id):
    training_program_details = get_object_or_404(TrainingProgram, id=trainingprogram_id)
    assignees = EmployeeTrainingProgram.objects.filter(trainingProgram_id=training_program_details.id)
    attendees = []
    for emp in assignees:
        person = Employee.objects.get(id=emp.id)
        attendees.append(person)
    context = {'training_program_details': training_program_details, 'attendees': attendees}
    return render(request, 'Bangazon/past_indiv_training_program.html', context)

# Displays form that creates a new training program
def new_training_program_form(request):
    form = NewTrainingForm()
    return render(request, 'Bangazon/new_training_program_form.html', {'form': form})

# Saves new program to database and forwards to training_programs
def save_program(request):
    training = TrainingProgram(name=request.POST['training_name'], description=request.POST['training_description'], startDate=request.POST['training_startDate'], endDate=request.POST['training_endDate'], maxEnrollment=request.POST['training_maxEnrollment'])
    training.save()
    return HttpResponseRedirect(reverse('Bangazon:training_programs'))

# Displays form with existing data prepopulated and allows user to edit details
def edit_training_details(request, trainingprogram_id):
    training_program_details = TrainingProgram.objects.get(id=trainingprogram_id)
    form = NewTrainingForm(initial={'training_name': training_program_details.name, 'training_description': training_program_details.description, 'training_startDate': training_program_details.startDate, 'training_endDate': training_program_details.endDate, 'training_maxEnrollment': training_program_details.maxEnrollment})
    return render(request, 'Bangazon/edit_training.html', {'form': form, "id": trainingprogram_id})

# Saves updated training details from edit_training_details form
def update_program(request):
    TrainingProgram.objects.filter(id=request.POST['trainingprogram_id']).update(name = request.POST['training_name'], description = request.POST['training_description'], startDate = request.POST['training_startDate'], endDate = request.POST['training_endDate'], maxEnrollment = request.POST['training_maxEnrollment'])
    return HttpResponseRedirect(reverse('Bangazon:training_programs'))

# Deletes upcoming training event
def training_delete(request):
    training = TrainingProgram.objects.get(id=request.POST['trainingprogram_id'])
    training.delete()
    return HttpResponseRedirect(reverse('Bangazon:training_programs'))