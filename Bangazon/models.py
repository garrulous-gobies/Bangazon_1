# Create your models here.
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create Department table
class Department(models.Model):
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
  departmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
  def __str__(self):
    return self

# Create Computer table
class Computer(models.Model):
  purchaseDate = models.DateTimeField()
  decommissionDate = models.DateTimeField()
  manufacturer = models.CharField(max_length = 50)
  model = models.CharField(max_length = 50)
  def __str__(self):
    return self

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
  def __str__(self):
    return self

# Create computerEmployee table
class ComputerEmployee(models.Model):
  employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
  computerId = models.ForeignKey(Computer, on_delete=models.CASCADE)

# Create Training Enrollment join table
class EmployeeTrainingProgram(models.Model):
  employeeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
  trainingProgramId = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
  status = models.CharField(max_length = 50)
  def __str__(self):
    return self
