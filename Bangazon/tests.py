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
        employee = Employee.objects.create(firstName="Fred", lastName="Frederickson", startDate="1991-02-13", isSupervisor=0, departmentId=department)

        response = Employee.objects.get(pk=1)
        self.assertEqual(response.id, employee.id)
        self.assertEqual(response.firstName, employee.firstName)
        self.assertEqual(response.lastName, employee.lastName)
        self.assertEqual(response.departmentId_id , department.id) #TODO: departmentId is changing in models

    def test_emp_detail_template(self):



class DepartmentListTest(TestCase):

  def test_department(self):
    def test_list_departments(self):

      department = Department.objects.create(name="Sales", budget=1999)
      employee = Employee.objects.create(firstName="Joe", lastName="Shep", startDate="1776-07-04", isSupervisor=1, departmentId=department)
      response = Department.objects.get(pk=1)

      self.assertEqual(department.name, response.name)
      self.assertEqual(department.budget, response.budget)

      self.assertEqual(len(response.context['department']), 1)
      self.assertIn(department.name.encode(), response.content)

      for emp in response.employee_set.all():
        self.assertEqual(employee.firstName, emp.firstName)


