# Create your models here.
from django.db import models
from django.utils import timezone


# Create Employee table
class employee(models.Model):
  firstName = models.CharField(max_length = 50)
  lastName = models.CharField(max_length = 50)
  startDate = models.DateTimeField()
  isSupervisor = models.ImageField(min_value = 0, max_value = 1)
  departmentId = models.ForeignKey(Department, on_delete=models.CASCADE)

  def __str__(self):
    return self

# Create computerEmployee table
class computerEmployee(models.Model):
  employeeId = models.ForeignKey(employee, on_delete=models.CASCADE)
  computerId = models.ForeignKey(computer, on_delete=models.CASCADE)

# Create Employee Type table (supervisor, non-supervisor)
class EmployeeType(models.Model):
  TypeName = models.CharField(max_length = 50)
  def __str__(self):
    return self

# Create Department table
class Department(models.Model):
  Budget = models.CharField(max_length = 50)
  DepartmentName = models.CharField(max_length = 50)
  def __str__(self):
    return self

# Create Computer table
class Computer(models.Model):
  AsigneeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
  AssignedToId = models.ForeignKey(Employee, on_delete=models.CASCADE)
  PurchaseDate = models.CharField(max_length = 50)
  DecommissionedDate = models.CharField(max_length = 50)
  Manufacturer = models.CharField(max_length = 50)
  Model = models.CharField(max_length = 50)
  def __str__(self):
    return self

# Create Training Enrollment join table
class TrainingEnrollment(models.Model):
  EmployeeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
  TrainingCourseId = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE)
  AsigneeId = models.ForeignKey(Employee, on_delete=models.CASCADE)
  Status = models.CharField(max_length = 50)
  def __str__(self):
    return self

# Create Training Course table
class TrainingCourse(models.Model):
  ProgramName = models.CharField(max_length = 50)
  ProgramDescription = models.CharField(max_length = 250)
  StartDate = models.CharField(max_length = 50)
  EndDate = models.CharField(max_length = 50)
  MaxEnrollment = models.IntegerRangeField(min_value=1, max_value=100)
  CurrentEnrollment = models.IntegerField(min_value=0, max_value=100)
  def __str__(self):
    return self