from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
from django.utils import timezone

from django.http import HttpResponse

# Create your views here.

                            #____________________________________________________________________________________________________________________
def homepage(request):
    return render(request,'index.html')

                            #____________________________________________________________________________________________________________________



def loginpage(request):
    error = ""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request,username=email,password=password)
        try :
            if user is not None:
                error = "no"
                login(request,user)
                g = request.user.groups.all()[0].name
                if g == 'Patients':
                  return render(request,'patienthome.html',{'error' : error})
                elif g == 'Doctors' :
                    return render(request,'doctorhome.html',{'error' : error})
                elif g == 'Receptionist' :
                    return render(request,'receptionhome.html',{'error' : error})
                elif g == 'Admin':
                    return render(request, 'adminhome.html', {'error': error})
                else:
                    error ="yes"
        except Exception as e:
            error="yes"

    return render(request,'login.html')


                        #____________________________________________________________________________________________________________________



def contactpage(request):
    return render(request, 'contact.html')


def Logout(request):
    logout(request)
    return redirect('loginpage')

                           #____________________________________________________________________________________________________________________



def createaccountpage(request):
    error = "nothing"
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        address = request.POST['address']
        phonenumber = request.POST['phonenumber']
        birthdate = request.POST['Bday']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword :
                Patient.objects.create(name=name,email=email,gender=gender,address=address,phonenumber=phonenumber,birthdate=birthdate,bloodgroup=bloodgroup)
                patient = User.objects.create_user(first_name=name,email=email,password=password,username=email)
                Group.objects.get(name='Patients').user_set.add(patient)
                patient.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"

    return render(request,'signup.html',{'error':error})

                            #____________________________________________________________________________________________________________________




def home(request):
    if request.user.is_staff:
       return render(request,'adminhome.html')
    elif request.user.is_active:
        g = request.user.groups.all()[0].name
        if g == 'Doctors':
          return render(request, 'doctorhome.html')
        elif g == 'Receptionist':
          return render(request, 'receptionhome.html')
        elif g == 'Patients':
          return render(request, 'patienthome.html')
    else:
        return redirect('loginpage')

                             #____________________________________________________________________________________________________________________



def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patients':
        patient_detail = Patient.objects.all().filter(email=request.user)

        return render(request,'patientprofile.html',{'patient_details':patient_detail})
    elif g == 'Doctors':
        doctor_detail = Doctor.objects.all().filter(email=request.user)

        return render(request,'doctorprofile.html',{'doctor_details':doctor_detail})
    elif g == 'Receptionist':
        receptionist_detail = Receptionist.objects.all().filter(email=request.user)

        return render(request,'receptionprofile.html',{'receptionist_details':receptionist_detail})

                             #____________________________________________________________________________________________________________________



def make_appointment(request):
    if not request.user.is_active:
        return redirect('loginpage')

    doctor_list = Doctor.objects.all()
    error =""
    if request.method == 'POST':
        temp = request.POST['doctoremail']
        doctoremail = temp.split()[0]
        doctorname =temp.split()[1]
        patientname = request.POST['patientname']
        patientemail = request.POST['patientemail']
        appdate = request.POST['appointmentdate']
        apptime = request.POST['appointmenttime']
        symtoms = request.POST['symtoms']
        try:
            appointment.objects.create(doctorname=doctorname,patientname=patientname,doctoremail=doctoremail,patientemail=patientemail,appointmentdate=appdate,appointmenttime=apptime,symptoms=symtoms,prescription="",status =True)
            error ="no"
        except Exception as e:
            error = "yes"
        return render(request,'patientmakeappointment.html',{'error':error })

    return render(request,'patientmakeappointment.html', {'doctor_list':doctor_list})

                             #____________________________________________________________________________________________________________________



def view_appointment(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patients':
        coming_a =appointment.objects.filter(patientemail=request.user,appointmentdate__gte =timezone.now(),status=True).order_by('appointmentdate')
        pre_a =appointment.objects.filter(patientemail=request.user,appointmentdate__lt =timezone.now()).order_by('-appointmentdate')| appointment.objects.filter(patientemail=request.user,status=False).order_by('-appointmentdate')
        return render(request,'patientviewappointments.html',{'coming_a':coming_a,'pre_a':pre_a})

    elif g == 'Doctors':
        if request.method == 'POST':
            add_pre = request.POST['prescription']
            app_id = request.POST['idofprescription']
            appointment.objects.filter(id=app_id).update(prescription=add_pre,status=False)
        coming_a = appointment.objects.filter(doctoremail=request.user,appointmentdate__gte=timezone.now(),status =True).order_by('appointmentdate')
        pre_a = appointment.objects.filter(doctoremail=request.user, appointmentdate__lt=timezone.now()).order_by('-appointmentdate')| appointment.objects.filter(doctoremail=request.user,status=False).order_by('-appointmentdate')
        return render(request, 'doctorviewappointment.html', {'coming_a': coming_a, 'pre_a': pre_a})


    elif g == 'Receptionist':
        coming_a =appointment.objects.filter(appointmentdate__gte =timezone.now(),status=True).order_by('appointmentdate')
        pre_a =appointment.objects.filter(appointmentdate__lt =timezone.now()).order_by('-appointmentdate')| appointment.objects.filter(status=False).order_by('-appointmentdate')
        return render(request,'receptionviewappointments.html',{'coming_a':coming_a,'pre_a':pre_a})


                             #____________________________________________________________________________________________________________________



def delete_appointment(request,a_id):
    app = appointment.objects.get(id=a_id)
    app.delete()
    return redirect('viewappointments')




def add_doctor(request):
    error = ""
    user = "none"
    if not request.user.is_staff:
        return redirect('loginpage')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['Bday']
        bloodgroup = request.POST['bloodgroup']
        specialization = request.POST['specialization']

        try:
            if password == repeatpassword:
                Doctor.objects.create(name=name, email=email, gender=gender, phonenumber=phonenumber,
                                      address=address, birthdate=birthdate, bloodgroup=bloodgroup,
                                      specialization=specialization)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                doc_group = Group.objects.get(name='Doctors')
                doc_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
    return render(request, 'adminadddoctor.html', {'error': error})



def add_receptionist(request):
    error = ""
    user = "none"
    if not request.user.is_staff:
        return redirect('loginpage')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['Bday']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword:
                Receptionist.objects.create(name=name, email=email, gender=gender, phonenumber=phonenumber,
                                      address=address, birthdate=birthdate, bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                rec_group = Group.objects.get(name='Receptionist')
                rec_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
    return render(request, 'adminaddreceptionist.html', {'error': error})




def adminviewReceptionist(request):
	if not request.user.is_staff:
		return redirect('loginpage')
	rec = Receptionist.objects.all()
	return render(request,'adminviewreceptionists.html',{ 'rec' : rec })




def adminviewdoctor(request):
	if not request.user.is_staff:
		return redirect('loginpage')

	rec = Doctor.objects.all()
	return render(request,'adminviewDoctors.html',{ 'rec' : rec })




def adminviewPatient(request):
	if not request.user.is_staff:
		return redirect('loginpage')

	rec = Patient.objects.all()
	return render(request,'adminviewPatients.html',{ 'rec' : rec })



def admin_delete_doctor(request,pid,email):
	if not request.user.is_staff:
		return redirect('loginpage')
	doctor = Doctor.objects.get(id=pid)
	doctor.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('view_doctor')



def admin_delete_patient(request,pid,email):
	if not request.user.is_staff:
		return redirect('loginpage')
	doctor = Patient.objects.get(id=pid)
	doctor.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('view_Patient')



def admin_delete_receptionist(request,pid,email):
	if not request.user.is_staff:
		return redirect('loginpage')
	doctor = Receptionist.objects.get(id=pid)
	doctor.delete()
	users = User.objects.filter(username=email)
	users.delete()
	return redirect('view_receptionist')
