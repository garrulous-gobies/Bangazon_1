from django.urls import path
from . import views

app_name = 'Bangazon'
urlpatterns = [
    path('Bangazon/Employees', views.employees, name='employees'),
    path('Bangazon/Employees/<int:employee_id>', views.employee_details, name='employee_details'),
    path('Bangazon/Employees/form', views.employee_form, name='employee_form'),
    path('Bangazon/Employees/new', views.employee_new, name='employee_new'),

    path('Bangazon/Departments', views.departments, name='departments'),
    path('Bangazon/Departments/NewDepartment', views.new_department, name='new_department'),
    path('Bangazon/Departments/SaveDepartment', views.save_department, name='save_department'),
    path('Bangazon/Departments/<int:department_id>', views.department_details, name='department_details'),

# ==================Computers==================================================
    path('Bangazon/Computers', views.computers, name='computers'),
    path('Bangazon/Computers/<int:computer_id>', views.computer_details, name='computer_details'),
    path('Bangazon/Computers/new', views.computer_new, name='computer_new'),
    path('Bangazon/Computers/form', views.computer_form, name='computer_form'),
    path('Bangazon/Computers/delete_confirm', views.computer_delete_confirm, name='computer_delete_confirm'),
    path('Bangazon/Computers/delete', views.computer_delete, name='computer_delete'),
# ===============================================================================================



    path('Bangazon/Training', views.training_programs, name='training_programs'),
    path('Bangazon/Training<int:pk>/', views.training_details, name='training_details'),
    path('Bangazon/TrainingPast<int:pk>/', views.past_training_details, name='past_training_details'),
    path('Bangazon/PastTraining', views.past_training_programs, name='past_training_programs'),
    path('Bangazon/NewTrainingClass', views.new_training_program_form, name='new_training_program_form'),
    path('Bangazon/SaveProgram', views.save_program, name='save_program'),
    path('Bangazon/EditTraining<int:pk>/', views.edit_training_details, name='edit_training_details'),
    path('Bangazon/UpdateProgram<int:pk>/', views.update_program, name='update_program'),
    path('Bangazon/DeleteProgram/<int:pk>', views.training_delete, name='training_delete'),
]

