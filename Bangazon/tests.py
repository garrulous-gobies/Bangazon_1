from django.test import TestCase
from .models import *
from django.urls import reverse
import unittest


# Create your tests here.
# What we should test
# context: what we send the template
# content: the rendered html
# resonse_codes

class EmployeeDetailsTests(TestCase):

    def test_emp_model(self):
        department = Department.objects.create(name="HR", budget=10)
        employee = Employee.objects.create(firstName="Fred", lastName="Frederickson", startDate="1991-02-13", isSupervisor=0, department=department)

        response = Employee.objects.get(pk=1)
        self.assertEqual(response.id, employee.id)
        self.assertEqual(response.firstName, employee.firstName)
        self.assertEqual(response.lastName, employee.lastName)
        self.assertEqual(response.department_id , department.id)


    def test_emp_detail_template(self):
        past_program = TrainingProgram.objects.create(name="Excel", description="Test description.", startDate="2012-01-28 14:30:00", endDate="2019-01-28 15:30:00", maxEnrollment=1)
        future_program = TrainingProgram.objects.create(name="Excel", description="Test description.", startDate="2020-03-28 14:30:00", endDate="2019-01-28 15:30:00", maxEnrollment=1)
        department = Department.objects.create(budget=1, name="IT")
        employee = Employee.objects.create(firstName="Brad", lastName="Davis", startDate="2019-01-01 08:00", isSupervisor=0, department= department)
        training = EmployeeTrainingProgram.objects.create(status="Pending", employee=employee, trainingProgram= past_program)
        training = EmployeeTrainingProgram.objects.create(status="Pending", employee=employee, trainingProgram= future_program)
        computer = Computer.objects.create(purchaseDate='2018-12-25 01:50:04', decommissionDate='2017-04-03 17:01:33', manufacturer='Micron', model='Chunk')
        employee_computer = Employee_Computer.objects.create(computer=computer, employee=employee)

        response = self.client.get(reverse('Bangazon:employee_details', args=(1,)))
        self.assertEqual(response.context['employee_details'].firstName, employee.firstName)
        self.assertEqual(response.context['employee_details'].lastName, employee.lastName)
        self.assertEqual(response.context['employee_details'].isSupervisor, employee.isSupervisor)
        self.assertEqual(response.context['employee_details'].computer, employee.computer)
        self.assertIn(past_program, response.context['past_training_programs'])
        self.assertIn(future_program, response.context['upcoming_training_programs'])




class DepartmentListTest(TestCase):

  def test_department(self):
    def test_list_departments(self):

      department = Department.objects.create(name="Sales", budget=1999)
      employee = Employee.objects.create(firstName="Joe", lastName="Shep", startDate="1776-07-04", isSupervisor=1, department=department)
      response = Department.objects.get(pk=1)

      self.assertEqual(department.name, response.name)
      self.assertEqual(department.budget, response.budget)

      self.assertEqual(len(response.context['department']), 1)
      self.assertIn(department.name.encode(), response.content)

      for emp in response.employee_set.all():
        self.assertEqual(employee.firstName, emp.firstName)



class DepartmentListTest(TestCase):

    def test_department(self):

        def test_list_departments(self):

            department = Department.objects.create(name="Sales", budget=1999)
            employee = Employee.objects.create(firstName="Joe", lastName="Shep", startDate="1776-07-04", isSupervisor=1, department=department)
            response = Department.objects.get(pk=1)

            self.assertEqual(department.name, response.name)
            self.assertEqual(department.budget, response.budget)

            self.assertEqual(len(response.context['department']), 1)
            self.assertIn(department.name.encode(), response.content)

            for emp in response.employee_set.all():
                self.assertEqual(employee.firstName, emp.firstName)



class TrainingListTest(TestCase):

    def test_list_trainings(self):

        program = TrainingProgram.objects.create(name="Excel", description="Test description.", startDate="2019-01-28 14:30:00", endDate="2019-01-28 15:30:00", maxEnrollment=1)

        response = TrainingProgram.objects.get(pk=1)
        self.assertEqual(program, response)

class TrainingWithAttendeesTest(TestCase):

    def test_trainings_with_attendees(self):

        program = TrainingProgram.objects.create(name="Excel", description="Test description.", startDate="2019-01-28 14:30:00", endDate="2019-01-28 15:30:00", maxEnrollment=1)
        department = Department.objects.create(budget=1, name="IT")
        employee = Employee.objects.create(firstName="Brad", lastName="Davis", startDate="2019-01-01 08:00", isSupervisor=0, department_id=1)
        training = EmployeeTrainingProgram.objects.create(status="Pending", employee_id= 1, trainingProgram_id= 1)

        training_attendees = EmployeeTrainingProgram.objects.filter(trainingProgram_id = 1)

        response = EmployeeTrainingProgram.objects.get(pk=1)
        self.assertEqual(training, response)

        response = self.client.get(reverse('Bangazon:past_training_programs'))
        self.assertEqual(response.status_code, 200)


class SaveTrainingProgramTest(TestCase):


    # Valid Form Data
    def test_add_training_validform_view(self):
        response = self.client.post(reverse('Bangazon:save_program'), {"training_name": "Test Name",
        "training_description": "Class description",
        "training_startDate": "2010-01-01 12:00:00",
        "training_endDate": "2011-01-01 12:00:00",
        "training_maxEnrollment": 5})
        with self.assertRaises(Exception) as context:
            broken_function()
        self.assertFalse('ValueError: invalid literal for int() with base 10:' in str(context.exception))


    def test_new_training_save(self):

        response = self.client.post(reverse('Bangazon:save_program'), {"training_name": "Test Name",
        "training_description": "Class description",
        "training_startDate": "2010-01-01 12:00:00",
        "training_endDate": "2011-01-01 12:00:00",
        "training_maxEnrollment": 5})

        self.assertEqual(response.status_code, 302)


class AddingDepartmentTest(TestCase):

    def test_add_department(self):
        response = self.client.post(reverse('Bangazon:save_department'), {"department_name":"Broccoli Sales", "department_budget": 100000})

        self.assertEqual(response.status_code, 302)

class AddingEmployeeTest(TestCase):

    def new_employee_status(self):
        department = Department.objects.create(name="Sadness", budget=5000)
        employee = Employee.objects.create(firstName="Joel", lastName="Shepdog", startDate="1996-07-01", isSupervisor=0, department=department)

        response = self.client.post(employee)

        self.assertEqual(response.status_code, 302)

class EmployeeFormTest(TestCase):
    def test_employee_form(self):
        response = self.client.get(reverse('Bangazon:employee_form'))
        self.assertIn(
            '<input type="text" name="firstName" id="employee_new_first_name" required=True>'.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="lastName" id="employee_new_last_name" required=True>'.encode(), response.content
        )
        self.assertIn(
            '<input type="datetime-local" name="startDate" id="employee_new_start_date" required=True>'.encode(), response.content
        )
        self.assertIn(
            '<select name="supervisor" id="employee_new_supervisor">'.encode(), response.content
        )
        self.assertIn(
            '<select name="department" id="employee_new_department" required=True>'.encode(), response.content
        )

class EmployeeListTest(TestCase):
    def test_employee_list(self):
        department = Department.objects.create(name="Fun", budget=100001)
        employee = Employee.objects.create(firstName="Joe", lastName="Shep", startDate="1900-01-04", isSupervisor=1, department=department)
        response = Employee.objects.get(pk=1)

        self.assertEqual(employee.firstName, response.firstName)
        self.assertEqual(department.name, response.department.name)