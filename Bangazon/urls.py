from django.urls import path

from . import views

app_name = 'Bangazon'
urlpatterns = [
    path('Bangazon/Employees', views.employees, name='employees'),
    path('Bangazon/Employees/<int:employee_id>', views.employee_details, name='employee_details'),
    path('Bangazon/Departments', views.departments, name='departments'),
    path('Bangazon/Computers', views.computers, name='computers'),
    path('Bangazon/Training', views.training_programs, name='training_programs'),
    path('Training<int:pk>/', views.training_details, name='training_details'),
    path('Bangazon/PastTraining', views.past_training_programs, name='past_training_programs'),
]
