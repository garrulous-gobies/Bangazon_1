from django.test import TestCase
from .models import *
from django.urls import reverse
import unittest





# ===============================TRAINING========================================

# Tests creation of training program and the redirect after the save
class TrainingListTest(TestCase):
    def test_list_trainings(self):
        response = self.client.post(reverse('Bangazon:save_program'), {"training_name": "Test Name", "training_description": "Class description", "training_startDate": "2010-01-01 12:00:00", "training_endDate": "2011-01-01 12:00:00", "training_maxEnrollment": 5})
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('Bangazon:training_programs'))
        self.assertEqual(response.status_code, 200)


# Tests creation of training program, saving of department, saving of new employee, and saving of training program assignment. as well as redirect to past training page
class TrainingWithAttendeesTest(TestCase):
    def test_trainings_with_attendees(self):
        response = self.client.post(reverse('Bangazon:save_program'), {"training_name": "Test Name", "training_description": "Class description", "training_startDate": "2010-01-01 12:00:00", "training_endDate": "2011-01-01 12:00:00", "training_maxEnrollment": 5})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('Bangazon:save_department'), {
                                    "department_name": "IT", "department_budget": 100000})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('Bangazon:employee_new'), {"firstName":"Brad", "lastName":"Davis", "startDate":"2019-01-01 08:00", "supervisor":0, "department":1})
        self.assertEqual(response.status_code, 302)

        training = EmployeeTrainingProgram.objects.create(
            status="Pending", employee_id=1, trainingProgram_id=1)

        training_attendees = EmployeeTrainingProgram.objects.filter(
            trainingProgram_id=1)
        response = EmployeeTrainingProgram.objects.get(pk=1)
        self.assertEqual(training, response)

        response = self.client.get(reverse('Bangazon:past_training_programs'))
        self.assertEqual(response.status_code, 200)



# Tests the validity of the data that is sent from the form as well as program saving
class SaveTrainingProgramTest(TestCase):
    def test_add_training_validform_view(self):
        response = self.client.post(reverse('Bangazon:save_program'), {"training_name": "Test Name", "training_description": "Class description", "training_startDate": "2010-01-01 12:00:00", "training_endDate": "2011-01-01 12:00:00", "training_maxEnrollment": 5})
        with self.assertRaises(Exception) as context:
            broken_function()
        self.assertFalse(
            'ValueError: Error with add training valid form test:' in str(context.exception))
        self.assertEqual(response.status_code, 302)

    def test_new_training_save(self):
        response = self.client.post(reverse('Bangazon:save_program'), {"training_name": "Test Name", "training_description": "Class description", "training_startDate": "2010-01-01 12:00:00", "training_endDate": "2011-01-01 12:00:00", "training_maxEnrollment": 5})
        self.assertEqual(response.status_code, 302)



# Tests the saving of a training class as well as the edit of a training class
class TrainingEditTest(TestCase):
    def test_edit_trainings(self):
        program = {'training_name': "Test Name", 'training_description': "Class description", 'training_startDate': "2010-01-01 12:00:00", 'training_endDate': "2011-01-01 12:00:00", 'training_maxEnrollment': 5}
        response = self.client.post(reverse('Bangazon:save_program'), program)

        self.assertEqual(response.status_code, 302)

        details = TrainingProgram.objects.get(pk=1)
        self.assertEqual(program['training_name'], details.name)

        pk = 1
        response = TrainingProgram.objects.filter(id=pk).update(name="Excel", description="Test description.", startDate="2019-01-28 14:30:00", endDate="2019-01-28 15:30:00", maxEnrollment=0)
        secondDetails = TrainingProgram.objects.get(pk=1)
        self.assertEqual(secondDetails.name, "Excel")


        self.assertEqual(response, 1)






# ===============================DEPARTMENT========================================
class AddingDepartmentTest(TestCase):
    def test_add_department(self):
        response = self.client.post(reverse('Bangazon:save_department'), {
                                    "department_name": "Broccoli Sales", "department_budget": 100000})
        self.assertEqual(response.status_code, 302)
    def test_add_department_form(self):
        response = self.client.get(reverse('Bangazon:new_department'))
        self.assertIn(
          '<input name="department_name" type="text" placeholder="Department Name" required=True>'.encode(), response.content)
        self.assertIn(
          '<input name="department_budget" type="number" placeholder="Department Budget" required=True>'.encode(), response.content)


class DepartmentDetails(TestCase):
    def test_department_details(self):

        department = Department.objects.create(name="Heavy Metals", budget=2)
        employee = Employee.objects.create(
            firstName="Bryan", lastName="Nilsen", startDate="1971-01-02", isSupervisor=1, department=department)

        response = self.client.get(
            reverse('Bangazon:department_details', args=(1,)))
        self.assertEqual(
            response.context['department_details'].name, department.name)
        self.assertEqual(
            response.context['department_details'].budget, department.budget)


        for emp in response.context['department_details'].employee_set.all():
            self.assertEqual(emp.firstName, employee.firstName)
            self.assertEqual(emp.lastName, employee.lastName)
            self.assertEqual(emp.department, employee.department)


class DepartmentListTest(TestCase):

    def test_department(self):
        def test_list_departments(self):

            department = Department.objects.create(name="Sales", budget=1999)
            employee = Employee.objects.create(
                firstName="Joe", lastName="Shep", startDate="1776-07-04", isSupervisor=1, department=department)
            response = Department.objects.get(pk=1)

            self.assertEqual(department.name, response.name)
            self.assertEqual(department.budget, response.budget)

            self.assertEqual(len(response.context['department']), 1)
            self.assertIn(department.name.encode(), response.content)

            for emp in response.employee_set.all():
                self.assertEqual(employee.firstName, emp.firstName)






# ===============================EMPLOYEE========================================
class AddingEmployeeTest(TestCase):
    def new_employee_status(self):
        department = Department.objects.create(name="Sadness", budget=5000)
        employee = Employee.objects.create(
            firstName="Joel", lastName="Shepdog", startDate="1996-07-01", isSupervisor=0, department=department)
        response = self.client.post(employee)
        self.assertEqual(response.status_code, 302)

class EmployeeDetailsTests(TestCase):

    def test_emp_model(self):
        """Tests the Employee model for expected columns and values

        Author(s): Nolan Little
        """

        department = Department.objects.create(name="HR", budget=10)
        employee = Employee.objects.create(
            firstName="Fred", lastName="Frederickson", startDate="1991-02-13", isSupervisor=0, department=department)

        response = Employee.objects.get(pk=1)
        self.assertEqual(response.id, employee.id)
        self.assertEqual(response.firstName, employee.firstName)
        self.assertEqual(response.lastName, employee.lastName)
        self.assertEqual(response.department_id, department.id)

    def test_emp_detail_view(self):

        """Tests context of the employee detail view for expected contents

        Author(s): Nolan Little
         """

        past_program = TrainingProgram.objects.create(
            name="Excel", description="Test description.", startDate="2012-01-28 14:30:00", endDate="2019-01-28 15:30:00", maxEnrollment=1)
        future_program = TrainingProgram.objects.create(
            name="Excel", description="Test description.", startDate="2020-03-28 14:30:00", endDate="2019-01-28 15:30:00", maxEnrollment=1)
        department = Department.objects.create(budget=1, name="IT")
        employee = Employee.objects.create(
            firstName="Brad", lastName="Davis", startDate="2019-01-01 08:00", isSupervisor=0, department=department)
        training_past = EmployeeTrainingProgram.objects.create(
            status="Pending", employee=employee, trainingProgram=past_program)
        training_future = EmployeeTrainingProgram.objects.create(
            status="Pending", employee=employee, trainingProgram=future_program)
        computer = Computer.objects.create(
            purchaseDate='2018-12-25 01:50:04', decommissionDate='2017-04-03 17:01:33', manufacturer='Micron', model='Chunk')
        employee_computer = Employee_Computer.objects.create(
            computer=computer, employee=employee)

        response = self.client.get(
            reverse('Bangazon:employee_details', args=(1,)))
        self.assertEqual(
            response.context['employee_details'].firstName, employee.firstName)
        self.assertEqual(
            response.context['employee_details'].lastName, employee.lastName)
        self.assertEqual(
            response.context['employee_details'].isSupervisor, employee.isSupervisor)
        self.assertEqual(
            response.context['employee_details'].computer, employee.computer)
        self.assertIn(past_program, response.context['past_training_programs'])
        self.assertIn(future_program,
                      response.context['upcoming_training_programs'])

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
        employee = Employee.objects.create(
            firstName="Joe", lastName="Shep", startDate="1900-01-04", isSupervisor=1, department=department)
        response = Employee.objects.get(pk=1)

        self.assertEqual(employee.firstName, response.firstName)
        self.assertEqual(department.name, response.department.name)


class EditEmployeeTest(TestCase):
    def test_emp_edit(self):

        department = Department.objects.create(name="Chicago", budget=1500000)
        employee = Employee.objects.create(firstName="Elyse", lastName="Dawson", startDate="1999-04-10", isSupervisor=1, department=department)

        details = Employee.objects.get(pk=1)
        self.assertEqual(employee, details)

        pk = 1

        response = Employee.objects.filter(id=pk).update(firstName="Big E", lastName="Dawson", startDate="2011-01-10", isSupervisor=1, department=department)

        self.assertEqual(response, 1)

        secondDetails = Employee.objects.get(pk=1)
        self.assertEqual(secondDetails.firstName, "Big E")

    def test_emp_edit_via_form_submit(self):

        department = Department.objects.create(name="Kentucky", budget=5)
        employee = Employee.objects.create(firstName="Brendan", lastName="McCray", startDate="1999-04-10", isSupervisor=1, department=department)

        dept = Department.objects.get(pk=1)

        self.assertEqual(department, dept)

        response = self.client.post(reverse('Bangazon:employee_update', args=(1,)), {'id':1, 'firstName': 'Brondan', 'lastName': 'McCray', 'startDate': '1999-04-10', 'supervisor': 1, 'department': dept.id})

        self.assertEqual(response.status_code, 302)



class EmployeeEditFormTest(TestCase):
    def test_employee_edit_form(self):
        department = Department.objects.create(name="Hydroflask", budget=1500000)
        employee = Employee.objects.create(firstName="Daniel", lastName="Combs", startDate="1999-04-10", isSupervisor=1, department=department)

        response = self.client.get(reverse('Bangazon:employee_edit', args=(1,)))
        self.assertIn(
            '<input type="text" name="firstName" value="Daniel" maxlength="35" required id="id_firstName">'.encode(), response.content
        )
        self.assertIn(
            'input type="text" name="lastName" value="Combs" maxlength="35" required id="id_lastName">'.encode(), response.content
        )






# ===============================COMPUTERS========================================

class ComputerDetailsTests(TestCase):
    """Test computer details page

        Model: Computer, Employee, Department

        Template: all of the computer templates

        Author(s): Jase Hackman
        """

    def test_comp_model(self):
        """
        Purpose:Test that the computer model can save a new computer

        Arguments: Self

        Author(s): Jase Hackman

        """

        computer = Computer(purchaseDate = "2016-01-20 08:00:00", decommissionDate= "2016-01-20 08:00:00", manufacturer="dell", model="xps15")
        computer.save()
        response = Computer.objects.get(pk=1)
        self.assertEqual(response, computer)

    def test_comp_detail(self):

        """
        Purpose:Test that the details page gets the correct response code and the correct information is sent to it.

        Arguments: Self

        Author(s): Jase Hackman

        """
        computer = Computer(purchaseDate = "2016-01-20 08:00:00", decommissionDate= "2016-01-20 08:00:00", manufacturer="dell", model="xps15")
        computer.save()
        response = self.client.get(reverse('Bangazon:computer_details', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["computer"], computer)

    def test_comp_form(self):

        """
        Purpose:Test that the form populates the correct fields

        Arguments: Self

        Author(s): Jase Hackman

        """

        response= self.client.get(reverse('Bangazon:computer_form'))
        self.assertIn(
            '<input type="text" name="model" id="computer_new_model">'.encode(), response.content
        )
        self.assertIn(
            '<input type="text" name="manufacturer" id="computer_new_manufacturer">'.encode(), response.content
        )
        self.assertIn(
            '<input type="datetime-local" name="purchase" id="computer_new_purchase">'.encode(), response.content
        )
        self.assertIn(
            '<input type="datetime-local" name="purchase" id="computer_new_purchase">'.encode(), response.content
        )

    def test_comp_add(self):

        """
        Purpose:Test that the add computer to an emmployee works correctly and gets back the correct status code.

        Arguments: Self

        Author(s): Jase Hackman

        """

        department = Department.objects.create(name="HR", budget=10)
        Employee.objects.create(firstName="Fred", lastName="Frederickson", startDate="1991-02-13", isSupervisor=0, department=department)
        response = self.client.post(reverse('Bangazon:computer_new'),
        {
        "purchase": "2010-01-01 12:00:00",
        "model": "XPS15",
        "manufacturer": "Dell",
        "assignment": 1})

        self.assertEqual(response.status_code, 302)

class ComputerDelete(TestCase):


    """Test computer Delete

        Model: Computer

        Template: redirects to computers.html



        Author(s): Jase Hackman
        """

    def test_comp_delete(self):

        """
        Purpose:Test that a computer deletes properly

        Arguments: Self

        Author(s): Jase Hackman

        """
        computer = Computer(purchaseDate = "2016-01-20 08:00:00", decommissionDate= "2016-01-20 08:00:00", manufacturer="dell", model="xps15")
        computer.save()
        response = Computer.objects.get(pk=1)
        responseLength= Computer.objects.all()
        self.assertEqual(computer,response)
        delete = response = self.client.post(reverse('Bangazon:computer_delete'),
        {
        'computer_id':1})
        self.assertEqual(delete.status_code, 302)
        response2 = Computer.objects.all()
        self.assertNotEqual(responseLength, response2)


class ComputerFilterTest(TestCase):
    """Tests the behavior of the filter on the computer list view

        Author(s): Austin Zoradi, Nolan Little
    """

    def test_computer_filter(self):
        computer  = Computer(purchaseDate = "2016-01-20 08:00:00", decommissionDate= "2016-01-20 08:00:00", manufacturer="Dell", model="xpsBrick")
        computer2  = Computer(purchaseDate = "2016-01-20 08:00:00", decommissionDate= "2016-01-20 08:00:00", manufacturer="lenovo", model="paper weight")
        computer3  = Computer(purchaseDate = "2016-01-20 08:00:00", decommissionDate= "2016-01-20 08:00:00", manufacturer="Mac", model="pricebook")
        computer4  = Computer(purchaseDate = "2016-01-20 08:00:00", decommissionDate= "2016-01-20 08:00:00", manufacturer="HP", model="dusty")
        computer.save()
        computer2.save()
        computer3.save()
        computer4.save()

        # filter by manufacturer
        response = self.client.post(reverse('Bangazon:computers'), {
                                    'computer_search': 'dell'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(computer, response.context['computer_list'],)
        self.assertNotIn(computer2, response.context['computer_list'],)
        self.assertNotIn(computer3, response.context['computer_list'],)

        # filter by model
        response = self.client.post(reverse('Bangazon:computers'), {
                            'computer_search': 'pricebook'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(computer3, response.context['computer_list'],)
        self.assertNotIn(computer2, response.context['computer_list'],)
        self.assertNotIn(computer4, response.context['computer_list'],)
