from django.urls import path

from . import views

app_name="Bangazon"

urlpatterns = [
  path('employees', views.employees, name='employees'),
  path('departments', views.departments, name='departments'),
  path('computers', views.computers, name='computers'),
  path('training_programs', views.training_courses, name='training_programs')

]