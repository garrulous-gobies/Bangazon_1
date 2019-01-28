-- List of commands to fill out database

-- Add training program to database
INSERT into Bangazon_trainingprogram values ( null, "EEO", "This program is designed to teach employees about Equal Opportunity Employment. Training will cover protected classes, workplace diversity, and reporting protocol." , "2019-02-25 08:00:00", "2019-02-27 16:00:00", 50 )

-- Add employee to database
INSERT into Bangazon_employee values ( null, "Brad", "Davis" , "2018-01-20 08:00:00", 0, 1 )

-- Add training program to employee
INSERT into Bangazon_employeetrainingprogram values ( null, "Pending", 1 , 2 )

-- Add department to database
INSERT into Bangazon_department values ( null, 1000000, "Information Technology" )