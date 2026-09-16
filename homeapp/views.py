from django.shortcuts import render,redirect
from .models import *;
from django.conf import settings
from django.http import HttpResponse
import os
from django.shortcuts import render,redirect
from .models import *;
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
import random
from django. contrib import messages
from datetime import datetime,date, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from io import BytesIO
from django.core.files import File
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from .models import *
from adminapp.models import *
from .views import *
from event.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

#Home Page
def home_index(request):
    return render(request,'home/home_index.html')


#Register Page
def register(request):
    if request.method == 'POST':
        admin_reg = login_register()
        admin_reg.name = request.POST['name']
        admin_reg.address = request.POST['address']
        admin_reg.email = request.POST['email']
        admin_reg.password = random.SystemRandom().randint(100000, 999999)
        admin_reg.profile_pic = request.FILES['profile_pic']
        admin_reg.save()

        email_id=admin_reg.email
        passw=admin_reg.password

        subject = 'Greetings from Event Management'
        message = 'Congratulations,\nYou have successfully registered. \nYour login credentials \n\nEmail :'+str(email_id)+'\nPassword :'+str(passw)+'\n\nNote: This is a system generated email, do not reply to this email id.'
        email_from = settings.EMAIL_HOST_USER
        
        recipient_list = [email_id, ]
        send_mail(subject,message , email_from, recipient_list, fail_silently=True)
        return redirect('home_index')
        
    
        
    return render(request, 'home/register.html')
        
    

#Login Page
def login(request):
    admin = login_designation.objects.get(name="admin")
    # users = designation.objects.get(designation="users")
    if request.method == 'POST':
        # email  = request.POST['email']
        # password = request.POST['password']
        # user = authenticate(username=email,password=password)
        # if user is not None:
        #     request.session['SAdm_id'] = user.id
        #     return redirect( 'Admin_index')

        if login_register.objects.filter(email=request.POST['email'], password=request.POST['password'],designation=admin.id).exists():    
                
            Adm=login_register.objects.get(email=request.POST['email'], password=request.POST['password'])
            request.session['A_id'] = Adm.designation_id
            request.session['A_id'] = Adm.id 
            Adm=login_register.objects.get(id= Adm.id)
            
            return render(request,'admin/admin_dashboard.html',{'Adm':Adm})

        # elif login_register.objects.filter(email=request.POST['email'], password=request.POST['password'],designation=users.id).exists():
                
        #         usr=user_registration.objects.get(email=request.POST['email'], password=request.POST['password'])
        #         request.session['U_id'] = usr.designation_id
        #         request.session['U_id'] = usr.id 
        #         usr=user_registration.objects.filter(id= usr.id)
                
        #         return render(request,'user/user_dashboard.html',{'usr':usr})
        else:
            context = {'msg_error': 'Invalid data'}
            return render(request, 'home/login.html', context)
    return render(request,'home/login.html')



