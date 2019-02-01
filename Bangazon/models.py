# Create your models here.
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator



# Create Department table
class Department(models.Model):
    '''This is the representation of an instance of Department. A department has a name (a string) and budget (an interger) and an id.
    
    Author(s): Brad Davis, Jase Hackman, Zac Jones, Nolan Little, Austin Zoradi
    '''
    budget = models.IntegerField(
    default = 0,
    validators = [
      MaxValueValidator(1000000),
      MinValueValidator(0)
    ]
  )
    name = models.CharField(max_length = 50)
    def __str__(self):
        return self

# Create Computer table
class Computer(models.Model):
    purchaseDate = models.DateTimeField()
    decommissionDate = models.DateTimeField(null=True)
    manufacturer = models.CharField(max_length = 50)
    model = models.CharField(max_length = 50)
    def __str__(self):
        return self.model

# Create Employee table
class Employee(models.Model):
    firstName = models.CharField(max_length = 50)
    lastName = models.CharField(max_length = 50)
    startDate = models.DateTimeField()
    isSupervisor = models.IntegerField(
    default = 0,
    validators = [
        MaxValueValidator(1),
        MinValueValidator(0)
    ]
    )
    computer = models.ManyToManyField(Computer, through="Employee_Computer")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    def __str__(self):
        return self.firstName




# Create Training Course table
class TrainingProgram(models.Model):
  name = models.CharField(max_length = 50)
  description = models.CharField(max_length = 250)
  startDate = models.DateTimeField()
  endDate = models.DateTimeField()
  maxEnrollment = models.IntegerField(
    default = 0,
    validators = [
      MaxValueValidator(100),
      MinValueValidator(0)
    ]
  )
  employee = models.ManyToManyField(Employee, through="EmployeeTrainingProgram")
  def __str__(self):
    return self

class Employee_Computer(models.Model):
    employee=models.ForeignKey('Employee', on_delete=models.CASCADE)
    computer=models.ForeignKey('Computer', on_delete=models.CASCADE)
    assignDate=models.DateTimeField()
    removeDate=models.DateTimeField(null=True)

# Create Training Enrollment join table
class EmployeeTrainingProgram(models.Model):
  employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
  trainingProgram = models.ForeignKey('TrainingProgram', on_delete=models.CASCADE)
  status = models.CharField(max_length = 50)
  def __str__(self):
    return self
