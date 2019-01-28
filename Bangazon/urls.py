from django.urls import path

from . import views

app_name = 'Bangazon'
urlpatterns = [
    path('Bangazon/Employees', views.employees, name='employees'),
    path('Bangazon/Departments', views.departments, name='departments'),
    path('Bangazon/Computers', views.computers, name='computers'),
    path('Bangazon/Training', views.training_programs, name='training_programs'),
    path('Bangazon/Training<int:pk>/', views.training_details, name='training_details'),
    path('Bangazon/PastTraining', views.past_training_programs, name='past_training_programs'),
    path('Bangazon/NewTrainingClass', views.new_training_program_form, name='new_training_program_form'),
    path('Bangazon/SaveProgram', views.save_program, name='save_program'),
]