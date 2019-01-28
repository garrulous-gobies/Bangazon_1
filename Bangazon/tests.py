from django.test import TestCase
from .models import *
import unittest
from django.urls import reverse

# Create your tests here.
# What we should test
# context: what we send the template
# content: the rendered html
# resonse_codes


class DepartmentListTest(TestCase):

    def test_department(self):
        def test_list_departments(self):

            department = Department.objects.create(name="Sales", budget=1999)
            employee = Employee.objects.create(
                firstName="Joe", lastName="Shep", startDate="1776-07-04", isSupervisor=1, departmentId=department)
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
        employee = Employee.objects.create(firstName="Brad", lastName="Davis", startDate="2019-01-01 08:00", isSupervisor=0, departmentId_id=1)
        training = EmployeeTrainingProgram.objects.create(status="Pending", employeeId_id= 1, trainingProgramId_id= 1)

        training_attendees = EmployeeTrainingProgram.objects.filter(trainingProgramId_id = 1)

        response = EmployeeTrainingProgram.objects.get(pk=1)
        self.assertEqual(training, response)


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