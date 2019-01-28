from django.test import TestCase
from .models import *

# Create your tests here.

class EmployeeDetailsTests(TestCase):

    def test_emp_model(self):
        department = Department.objects.create(name="HR", budget=10)
        employee = Employee.objects.create(firstName="Fred", lastName="Frederickson", startDate="1991-02-13", isSupervisor=0, departmentId=department)

        response = Employee.objects.get(pk=1)
        self.assertEqual(response.id, employee.id)
        self.assertEqual(response.firstName, employee.firstName)
        self.assertEqual(response.lastName, employee.lastName)
        self.assertEqual(response.departmentId_id , department.id) #TODO: departmentId is changing in models
