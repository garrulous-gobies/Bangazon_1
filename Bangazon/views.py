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
    """Renders main landing page for Bangazon

    Model:None

    Template:index.html

    Author(s): Brad Davis
    """
    return render(request, 'Bangazon/index.html')


# ======================== EMPLOYEES ================


def employees(request):
    """Lists all employees in the database

    Model:Employee

    Template:employees.html

    Author(s): Zac Jones
    """

    employee_list = Employee.objects.all().order_by('lastName')
    context = {'employee_list': employee_list}
    return render(request, 'Bangazon/employees.html', context)


def employee_details(request, employee_id):
    """view method for an employee's details

    model(s): Employee, Computer, TrainingProgram

    template: employee_details.html

    Arguments:
        request {httprequest}
        employee_id {int} -- id of employee reversed from url path

    Returns:
        render -- html with the employee_details, past_training_programs, and upcoming_training_programs as context

    Author(s): Nolan Little
    """

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
    """Calls new employee form, populates dropdown with list of departments

    Model:Employee, Department

    Template:employee_form.html

    Author(s): Zac Jones
    """

    departments = Department.objects.all()
    context = {"departments": departments}
    return render(request, "Bangazon/employees_form.html", context)


def employee_new(request):
    """Saves a new instance of Employee via POST to the db, redirects to the list of all instances of employee

    Model:Employee, Department

    Template: redirects back to employees.html

    Author(s): Zac Jones
    """

    department = Department.objects.get(pk=request.POST['department'])
    employee = Employee(firstName = request.POST['firstName'], lastName = request.POST['lastName'], startDate = request.POST['startDate'], isSupervisor = request.POST['supervisor'], department = department)

    employee.save()
    return HttpResponseRedirect(reverse('Bangazon:employees'))


def employee_update(request, pk):
    """Saves an edited instance of Employee via POST to the db, redirects to the list of all instances of employee

    Model:Employee, Department, Computers, Training

    Template: redirects back to employees.html

    Author(s): Zac Jones, Nolan Little
    """

    department = Department.objects.get(pk=request.POST['department'])
    employee_edited = Employee(id=pk, firstName = request.POST['firstName'], lastName = request.POST['lastName'], startDate = request.POST['startDate'], isSupervisor = request.POST['supervisor'], department = department)

    employee_edited.save()
    return HttpResponseRedirect(reverse('Bangazon:employees'))


def employee_edit(request, pk):
    """Saves a new instance department via POST to the db, redirects to the list of all instances of department

    Model:Employee, Department, Computers, Training

    Template: redirects back to departments.html

    * Module is currently incomplete - still needs training assignments fix *

    Author(s): Zac Jones, Nolan Little
    """

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
        train_list.append((program.id, f'{program.name} \n beginning:{program.startDate}'))


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
    """Returns a list of all departments

    Model:Department

    Template:departments.html

    Author(s): Austin Zoradi
    """

    department_list = Department.objects.all().order_by('name')
    context = {'department_list': department_list}
    return render(request, 'Bangazon/departments.html', context)


def new_department(request):
    """Generates a form to add a new department to the db

    Model:Department

    Template:new_department_form.html

    Author(s): Austin Zoradi
    """
    department_list = Department.objects.all()
    context = {'department_list': department_list}
    return render(request, 'Bangazon/new_department_form.html', context)


def save_department(request):
    """Saves a new instance department via POST to the db, redirects to the list of all instances of department

    Model:Department

    Template: redirects back to departments.html

    Author(s): Austin Zoradi
    """
    name = request.POST['department_name']
    budget = request.POST['department_budget']
    handleIntBudget = int(str(budget).split(".")[0])
    dep = Department(name=name, budget=handleIntBudget)
    dep.save()
    return HttpResponseRedirect(reverse('Bangazon:departments'))


def department_details(request, department_id):
    """Returns a list of the details of an instance of a single department and the employee instances associated with it

    Model:Department

    Template:departments_details.html

    Author(s): Austin Zoradi
    """
    department_details = Department.objects.get(pk=department_id)
    context = {'department_details': department_details}
    return render(request, 'Bangazon/department_details.html', context)

def department_edit(request, department_id):
    """Returns an edit form prepopulated with data of the department that is going to be edited

    Arguments: department_id {[pk]} -- id of the department that is to be edited

    Model:Department

    Template:edit_department_form.html
    """
    department = Department.objects.get(id=department_id)
    context = {"department": department}
    return render(request, 'Bangazon/edit_department_form.html', context)

def department_update(request, department_id):
    """Updates the instance of department with id department_id with the new input values from the form in the db, rerenders department list

    Arguments: department_id {[pk]} -- id of the department that is to be edited

    Model:Department

    Template:edit_department_form.html
    """
    budget=request.POST['department_budget']
    handleIntBudget = int(str(budget).split(".")[0])
    edited_dept = Department(id=department_id, name=request.POST['department_name'], budget=handleIntBudget)
    edited_dept.save()
    return HttpResponseRedirect(reverse('Bangazon:departments'))

# ==========================COMPUTERS=================================


def computers(request):
    """Calls in main computer page and has function for filters

    Model:Computer

    Template:computers.html

    Author(s): Jase Hackman, Nolen Little, Austin Zoradi
    """
    if request.POST:
        computer_list = Computer.objects.filter(Q(manufacturer__icontains=request.POST['computer_search']) | Q(model__icontains=request.POST['computer_search']))
    else:
        computer_list = Computer.objects.all()

    context = {'computer_list': computer_list}
    return render(request, 'Bangazon/computers.html', context)


def computer_details(request, computer_id):
    """Renders computer details page

    Model:Computer

    Template:computers_details.html

    Author(s): Jase Hackman
    """
    computer = get_object_or_404(Computer, pk=computer_id)
    current_assignment_list = list()
    for rel in computer.employee_computer_set.all():
        current_assignment_list.append(rel.removeDate)
    print(current_assignment_list)
    context = {'computer': computer,
                'relationships': current_assignment_list
    }
    return render(request, 'Bangazon/computer_details.html', context)


def computer_form(request):
    """Calls new computer form and filters data so only employees without computers appear in dropdown.

    Model:Employee, Employe_Computer

    Template:computers_form.html

    Author(s): Jase Hackman
    """
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
    """Creates new computer in data base and redirects to main computer page.

    Model:Computer, Employee, Employe_Computer

    Template:none

    Author(s): Jase Hackman
    """
    computer = Computer(
        purchaseDate=request.POST['purchase'], model=request.POST['model'], manufacturer=request.POST['manufacturer'])
    computer.save()
    if request.POST['assignment'] != 'null':
        employee = Employee.objects.get(pk=request.POST['assignment'])
        relationship = Employee_Computer(employee=employee, computer=computer, assignDate=datetime.datetime.now())
        relationship.save()
    return HttpResponseRedirect(reverse('Bangazon:computers'))


def computer_delete_confirm(request):
    """Gets computer object for the computer you want to delete

    Model:Computer

    Template:computer_delete_confirm.html

    Author(s): Jase Hackman
    """
    computer= Computer.objects.get(pk=request.POST['computer_id'])
    is_assigned=computer.employee_set.all()
    assigned = False
    if len(is_assigned) > 0:
        assigned = True
    context = {'computer': computer,
                'assigned': assigned}
    return render(request, "Bangazon/computer_delete_confirm.html", context)


def computer_delete(request):
    """Deletes computer, calls main computer function.

    Model:Computer

    Template:none

    Author(s): Jase Hackman
    """
    computer= Computer.objects.get(pk=request.POST['computer_id'])
    computer.delete()
    return HttpResponseRedirect(reverse('Bangazon:computers'))

def computer_decommision(request):
    """Decomissions a computer

    Model: Computer

    template: None

    Author: Jase Hackman
    """

    computer= Computer.objects.filter(pk=request.POST['computer_id'])
    computer.update(decommissionDate=datetime.datetime.now())
    return HttpResponseRedirect(reverse('Bangazon:computer_details', args=(request.POST['computer_id'],)))

# ===========================TRAINING================================


# Lists all training programs for future classes
def training_programs(request):
    """Returns a list of all future training programs

    Model:TrainingProgram

    Template:training_program.html

    Author(s): Brad Davis
    """
    now = timezone.now()
    training_program_list = TrainingProgram.objects.filter(startDate__gte=now)
    context = {'training_program_list': training_program_list}
    return render(request, 'Bangazon/training_program.html', context)

# List past training programs that have taken place
def past_training_programs(request):
    """Returns a list of all past training programs

    Model:TrainingProgram

    Template:past_training_program.html

    Author(s): Brad Davis
    """
    now = timezone.now()
    training_program_list = TrainingProgram.objects.filter(startDate__lte=now)
    context = {'training_program_list': training_program_list}
    return render(request, 'Bangazon/past_training_programs.html', context)

# Show specific details for upcoming training classes with options to edit or delete
def training_details(request, trainingprogram_id):
    """Returns a detailed view of future training program and options to edit or deleted

    Model:TrainingProgram

    Template:indiv_training_program.html

    Author(s): Brad Davis
    """
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
    """Returns a detailed view of past training program and options to edit or deleted

    Model:TrainingProgram

    Template:past_indiv_training_program.html

    Author(s): Brad Davis
    """
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
    """Returns a form to create a new training program

    Model:TrainingProgram

    Template:new_training_program_form.html

    Author(s): Brad Davis
    """
    form = NewTrainingForm()
    return render(request, 'Bangazon/new_training_program_form.html', {'form': form})

# Saves new program to database and forwards to training_programs
def save_program(request):
    """Performs check on start and end dates and either saves data and returns to main training page or alerts user and redisplays form

    Model:TrainingProgram

    Template:training_program.html or new_training_program_form_error.html

    Author(s): Brad Davis
    """
    training_program_details = TrainingProgram(name=request.POST['training_name'], description=request.POST['training_description'], startDate=request.POST['training_startDate'], endDate=request.POST['training_endDate'], maxEnrollment=request.POST['training_maxEnrollment'])
    if training_program_details.startDate > training_program_details.endDate:
        form = NewTrainingForm(initial={'training_name': training_program_details.name, 'training_description': training_program_details.description, 'training_startDate': training_program_details.startDate, 'training_endDate': training_program_details.endDate, })
        return render(request, 'Bangazon/new_training_program_form_error.html', {'form': form})
    else:
        training_program_details.save()
        return HttpResponseRedirect(reverse('Bangazon:training_programs'))

# Displays form with existing data prepopulated and allows user to edit details
def edit_training_details(request, trainingprogram_id):
    """Returns a form view with future training data prepopulated for editing

    Model:TrainingProgram

    Template:edit_training.html

    Author(s): Brad Davis
    """
    training_program_details = TrainingProgram.objects.get(id=trainingprogram_id)
    form = NewTrainingForm(initial={'training_name': training_program_details.name, 'training_description': training_program_details.description, 'training_startDate': training_program_details.startDate, 'training_endDate': training_program_details.endDate, 'training_maxEnrollment': training_program_details.maxEnrollment})
    return render(request, 'Bangazon/edit_training.html', {'form': form, "id": trainingprogram_id})

# Saves updated training details from edit_training_details form
def update_program(request):
    """Returns a detailed view of future training program and options to edit or deleted

    Model:TrainingProgram

    Template:trainging_programs.html or edit_training_error.html

    Author(s): Brad Davis
    """
    training_program_details = TrainingProgram(name=request.POST['training_name'], description=request.POST['training_description'], startDate=request.POST['training_startDate'], endDate=request.POST['training_endDate'], maxEnrollment=request.POST['training_maxEnrollment'])
    if training_program_details.startDate > training_program_details.endDate:
        newId = request.POST['trainingprogram_id']
        form = NewTrainingForm(initial={'training_name': training_program_details.name, 'training_description': training_program_details.description, 'training_startDate': training_program_details.startDate, 'training_endDate': training_program_details.endDate})
        return render(request, 'Bangazon/edit_training_error.html', {'form': form, 'id': newId})
    else:
        TrainingProgram.objects.filter(id=request.POST['trainingprogram_id']).update(name = request.POST['training_name'], description = request.POST['training_description'], startDate = request.POST['training_startDate'], endDate = request.POST['training_endDate'], maxEnrollment = request.POST['training_maxEnrollment'])
        return HttpResponseRedirect(reverse('Bangazon:training_programs'))


# Deletes upcoming training event
def training_delete(request):
    """Deletes a future training program and returns to main training page

    Model:TrainingProgram

    Template:training_program.html

    Author(s): Brad Davis
    """
    training = TrainingProgram.objects.get(id=request.POST['trainingprogram_id'])
    training.delete()
    return HttpResponseRedirect(reverse('Bangazon:training_programs'))