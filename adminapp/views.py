from django.shortcuts import render,redirect
from .models import *;
from django.conf import settings
from django.http import HttpResponse,JsonResponse
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
from homeapp.models import *
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
def admin_view_list(request):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        view_customer = admin_Customer.objects.filter(admin_id=A_id)
        return render(request,'admin/admin_view_list.html',{'cust':view_customer})
    else:
        return redirect('/')

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

#Add Document Page
def admin_document(request,id):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        view_customer = admin_Customer.objects.filter(id=id)
        item = admin_decor_items.objects.filter(customer_id=id)
        custid = admin_decor_items.objects.filter(customer_id=id)
        return render(request,'admin/admin_document.html',{'cust':view_customer,'custid':custid,'item':item})
    else:
        return redirect('/')

#Add Decor Items
def admin_ajax_add_customer(request):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        desig = login_register.objects.get(id=A_id)

        if request.method=='POST':
            Add_cust = admin_Customer()
            Add_cust.customer_name = request.POST.get('custname')
            Add_cust.customer_address = request.POST.get('custaddress')
            Add_cust.customer_contact = request.POST.get('custcontact')
            Add_cust.customer_advance = request.POST.get('custadvance')
            Add_cust.admin_id = A_id
            Add_cust.save()
            return redirect('admin_view_document')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})
    else:
            return redirect('/')

#Add Decor Items Ajax
def admin_ajax_add_quotation(request):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        desig = login_register.objects.get(id=A_id)
        adv = admin_Customer.objects.filter(id=A_id)
        ftotal = admin_decor_items.objects.filter(id=A_id,customer_id=adv.id)
        for j in ftotal:
            t=sum(j.item_total)
        advamt = 1000
        if request.method=='POST':
            Add_items = admin_decor_items()
            Add_items.item_name = request.POST.get('item')
            Add_items.item_qty = request.POST.get('qty')
            Add_items.item_price = request.POST.get('price')
            Add_items.branch_id = desig.branch.id
            Add_items.department_id = desig.department.id
            Add_items.designation_id = desig.designation.id
            Add_items.admin_id = A_id
            Add_items.customer_id = request.POST.get('cid')
            Add_items.item_total = int(Add_items.item_qty) * int(Add_items.item_price) 
            Add_items.item_final_amount = int(Add_items.item_total) - advamt



            Add_items.save()
            return redirect('admin_view_document')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})
    else:
            return redirect('/')

#Add Decor Items 
# def admin_ajax_add_quotation(request,id):
#     if 'A_id' in request.session:
#         if request.session.has_key('A_id'):
#             A_id = request.session['A_id']
#         else:
#             return redirect('/')
        
#         desig = login_register.objects.get(id=A_id)

#         if request.method=='POST':
#             Add_items = admin_decor_items()
#             Add_items.item_name = request.POST.get('item')
#             Add_items.item_qty = request.POST.get('qty')
#             Add_items.item_price = request.POST.get('price')
#             Add_items.branch_id = desig.branch.id
#             Add_items.department_id = desig.department.id
#             Add_items.designation_id = desig.designation.id
#             Add_items.admin_id = A_id
#             Add_items.customer_id = id
            
#             Add_items.item_total = int(Add_items.item_qty) * int(Add_items.item_price) 
#             # Add_items.item_final_amount = int(Add_items.item_total) - int(Add_items.item_advance) 



#             Add_items.save()
#             return JsonResponse({
#                 'success': True,
#                 'message': 'Quotation added successfully'
#             })
#         else:
#             return JsonResponse({'success': False, 'message': 'Invalid request method'})
#     else:
#             return redirect('/')

#Add Advance And Form Sbmit
def admin_add_AdvanceAndFormSubmit(request):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')    
        items = admin_decor_items.objects.filter(customer_id=id)
        a=[]
        a=items
        
        if request.method=='POST':
            Add_quot = admin_bill_amount()
            for j in a:
                Add_quot.item_final_amount = sum(1+9)
             


            Add_quot.save()
            return redirect('admin_view_list')
        
    