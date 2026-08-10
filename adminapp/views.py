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
from .views import *
from homeapp.views import *



#Admin Logout Page
def Admin_logout(request):
    if 'A_id' in request.session:  
        request.session.flush()
        return redirect("/")
    else:
        return redirect('/') 

#Add Branch Page
def admin_branch(request):
    return render(request,'home/branch.html')

#Add Department Page
def admin_department(request):
    return render(request,'home/department.html')

#Add Designation Page
def admin_designation(request):
    return render(request,'home/designation.html')

#Display Dashboard Page
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

#Add Document, list Document Page
def admin_view_document(request):
    return render(request,'admin/admin_view_document.html')

#View Document Page
def admin_view_pdf(request):

    
    template_path = 'admin/admin_view_pdf.html'
    context = {
    "background": os.path.join(settings.MEDIA_ROOT, "background4.jpg"),
    "background1": os.path.join(settings.MEDIA_ROOT, "background1.jpg"),
    "background2": os.path.join(settings.MEDIA_ROOT, "background2.jpg"),
    'media_url':settings.MEDIA_URL,
    
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'
    response['Content-Disposition'] = 'filename="file.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    


    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

