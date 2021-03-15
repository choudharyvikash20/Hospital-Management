from django.db import models

# Create your models here.

class Patient(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=16)
	gender = models.CharField(max_length=10)
	phonenumber = models.CharField(max_length=10)
	address = models.CharField(max_length=100)
	birthdate = models.DateField()
	bloodgroup = models.CharField(max_length=5)

	def __str__(self):
		return self.name

class Doctor(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	gender = models.CharField(max_length=10)
	address =models.CharField(max_length=150)
	phonenumber =models.CharField(max_length=10)
	birthdate = models.DateField()
	bloodgroup = models.CharField(max_length=5)
	specialization = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class appointment(models.Model):
	doctorname = models.CharField(max_length=50)
	patientname = models.CharField(max_length=50)
	doctoremail = models.EmailField()
	patientemail = models.EmailField()
	appointmentdate = models.DateField()
	appointmenttime = models.TextField()
	symptoms = models.CharField(max_length=150)
	prescription = models.CharField(max_length=200)
	status =models.BooleanField()

	def __str__(self):
		return "you  have an appointment with Dr. " + self.doctorname

class Receptionist(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	gender = models.CharField(max_length=10)
	address =models.CharField(max_length=150)
	phonenumber =models.CharField(max_length=10)
	birthdate = models.DateField()
	bloodgroup = models.CharField(max_length=5)

	def __str__(self):
		return self.name