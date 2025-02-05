

create database Med_Devices ; 

use Med_Devices ;
Go

create table Departments 
(
dep_id int not null ,
dep_name varchar (50) not null,
dep_location varchar (50) not null,
dep_head int not null,
constraint  Departments_pk primary key (dep_id)
);

create table Devices 
(
id int not null ,
D_name varchar (50) not null,
D_type varchar (50) not null,
man_comp varchar (50),
dep_id int NOT NULL,
per_charge int ,
next_maintenance_date date ,
D_classification varchar(50) NOT NULL,
room_number varchar(50) NOT NULL,
Serial_numebr varchar(50) NOT NULL,
D_status varchar(50) NOT NULL,
constraint  Devices_pk primary key (id)
);

create table Employees
(
emp_id int NOT NULL,
f_name varchar(50) NOT NULL,
l_name varchar(50) NOT NULL,
job_id int NOT NULL,
dep int NOT NULL,
email varchar(50) NOT NULL,
constraint  Employees_pk primary key (emp_id)
);


create table Invantory
(
device_id int NOT NULL ,
quantity int NOT NULL,
constraint  Invantory_pk primary key (device_id)
);

create table Maintenance_Records
(
Maintenance_id int NOT NULL IDENTITY (1,1),
device_id int NOT NULL,
Maintenance_date date NOT NULL,
technician int NOT NULL,
M_description varchar(50) NOT NULL,
constraint  Maintenance_Records_pk primary key (Maintenance_id)
);

create table Service_provider
(
provider_id int NOT NULL IDENTITY (1,1),
provider_name varchar(50) NOT NULL,
contact_infromation varchar(50) NOT NULL,
service_type varchar(50) NOT NULL,
device_id int NOT NULL,
constraint  Service_provider_pk primary key (provider_id)
);


create table job_desc
(
job_id int NOT NULL IDENTITY (1,1),
job_code varchar(50) NOT NULL,
job_description varchar(50) NOT NULL,
constraint  job_desc_pk primary key (job_id)
);


ALTER TABLE Devices 
ADD CONSTRAINT Devices_Employees_fk 
FOREIGN KEY (per_charge)
REFERENCES Employees (emp_id);

ALTER TABLE Devices
ADD CONSTRAINT Devices_Departments_fk
FOREIGN KEY (dep_id)
REFERENCES Departments (dep_id);

ALTER TABLE Employees
ADD CONSTRAINT Employees_job_desc_fk
FOREIGN KEY (job_id)
REFERENCES job_desc (job_id);


ALTER TABLE Employees
ADD CONSTRAINT Departments_Employees_fk 
FOREIGN KEY (dep)
REFERENCES Departments (dep_id);

ALTER TABLE Maintenance_Records
ADD CONSTRAINT Maintenance_Records_Devices_fk 
FOREIGN KEY (device_id)
REFERENCES Devices (id);

ALTER TABLE Maintenance_Records
ADD CONSTRAINT Maintenance_Records_Employees_fk 
FOREIGN KEY (technician)
REFERENCES Employees (emp_id);

ALTER TABLE Service_provider
ADD CONSTRAINT Service_provider_Devices_fk 
FOREIGN KEY (device_id)
REFERENCES Devices (id);



