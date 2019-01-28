from django.test import TestCase
from .models import *
import unittest

# Create your tests here.
# What we should test
# context: what we send the template
# content: the rendered html
# resonse_codes

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


class TrainingListTest(TestCase):

  def training_programs(self):

    def test_list_trainings(self):

      TrainingProgram.objects.create(name+)

    response = self.client.get(reverse('history:index'))

    self.assertEqual(response.status_code, 200)

    self.assertEqual(len(response.context['all_artists']), 1)

    self.assertIn(new_artist.ArtistName.encode(), response.content)

