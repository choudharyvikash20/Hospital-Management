
from django.contrib import admin
from django.urls import path
from hospital.views import *

from django.views.static import serve
from django.conf.urls import url
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='homepage'),
    path('login/', loginpage,name='loginpage'),
    path('contact/', contactpage,name='contactpage'),
    path('createaccount/',createaccountpage,name='createaccountpage'),
    path('logout/',Logout,name='logout'),
    path('home/',home,name='home'),
    path('home/profile/',profile,name='profile'),
    path('home/make_appointment/',make_appointment,name='makeappointment'),
    path('home/view_appointments/',view_appointment,name='viewappointments'),
    path('home/delete_appointment/<int:a_id>',delete_appointment,name='deleteappointment'),
    path('dashboard/add_doctor',add_doctor,name='add_doctor'),
    path('dashboard/add_receptionist',add_receptionist,name='add_receptionist'),
    path('dashboard/view_receptionist',adminviewReceptionist,name='view_receptionist'),
    path('dashboard/view_Patient',adminviewPatient,name='view_Patient'),
    path('dashboard/view_doctor',adminviewdoctor,name='view_doctor'),
    path('dashboard/delete_doctor<int:pid>,<str:email>',admin_delete_doctor,name='delete_doctor'),
    path('dashboard/delete_patient<int:pid>,<str:email>', admin_delete_patient, name='delete_patient'),
    path('dashboard/delete_receptionist<int:pid>,<str:email>', admin_delete_receptionist, name='delete_receptionist'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
