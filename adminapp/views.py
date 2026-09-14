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
from PIL import Image, ImageDraw
from io import BytesIO
import base64


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
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        log = login_register.objects.get(id=A_id)
        return render(request,'admin/admin_dashboard.html',{'log':log})
    else:
        return redirect('/')

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

#Helper function for image curved radius
def rounded_image(image_path, radius=30):
    image = Image.open(image_path).convert("RGBA")

    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, image.width, image.height),
        radius=radius,
        fill=255
    )

    rounded = Image.new("RGBA", image.size, (255, 255, 255, 0))
    rounded.paste(image, (0, 0), mask)

    output = BytesIO()
    rounded.save(output, format="PNG")

    encoded = base64.b64encode(output.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{encoded}"

#View Document Page
def admin_view_pdf(request,id):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        cus = admin_Customer.objects.get(id=id)
        cat = admin_Category.objects.filter(admin_id=id,admin_decor_items__customer_id=id).distinct()
        mitem = admin_decor_items.objects.filter(customer_id=id).select_related('item_category').order_by('item_category_id')
        sitem = admin_decor_subitems.objects.filter(customer_id=id)
        gall = admin_gallery.objects.filter(customer_id=id)
    
        for e in gall:
            e.rounded_img = rounded_image(
                e.gallery_img.path,
                radius=80
            )
        
        template_path = 'admin/admin_view_pdf.html'
        context = {
        "background": os.path.join(settings.MEDIA_ROOT, "background4.jpg"),
        "background1": os.path.join(settings.MEDIA_ROOT, "background1.jpg"),
        "background2": os.path.join(settings.MEDIA_ROOT, "background2.jpg"),
        'media_url':settings.MEDIA_URL,
        'cus': cus,
        'mitem': mitem,
        'sitem': sitem,
        'cat': cat,
        'gall': gall,
        
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
    else:
        return redirect('/')

#Add Document Page
def admin_document(request,id):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        view_customer = admin_Customer.objects.get(id=id)
        item = admin_decor_items.objects.filter(customer_id=id)
        cat = admin_Category.objects.filter(admin_id=A_id)
        custid = admin_decor_items.objects.filter(customer_id=id)
        return render(request,'admin/admin_document.html',{'cust':view_customer,'custid':custid,'item':item,'cat':cat})
    else:
        return redirect('/')

#Add customer
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
            Add_cust.customer_venue = request.POST.get('custvenue')
            Add_cust.customer_date = request.POST.get('custdate')
            Add_cust.customer_theme = request.POST.get('custtheme')
            Add_cust.customer_function_type = request.POST.get('custfunction')
            Add_cust.customer_contact = request.POST.get('custcontact')
            Add_cust.customer_advance = request.POST.get('custadvance')
            Add_cust.admin_id = A_id
            Add_cust.save()
            return redirect('admin_view_document')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})
    else:
            return redirect('/')

#Add customer
def admin_add_category(request):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        desig = login_register.objects.get(id=A_id)

        if request.method=='POST':
            Add_cat = admin_Category()
            Add_cat.category = request.POST.get('cat_name')
            Add_cat.admin_id = A_id
            Add_cat.save()
        return render(request,'admin/admin_add_category.html')
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
        
        if request.method=='POST':
            Add_items = admin_decor_items()
            Add_items.item_category_id = request.POST.get('mcat')
            Add_items.item_name = request.POST.get('item')
            Add_items.item_qty = request.POST.get('qty')
            Add_items.item_price = request.POST.get('price')
            Add_items.customer_id = request.POST.get('cid')
            advance = request.POST.get('cadv')
            Add_items.branch_id = desig.branch.id
            Add_items.department_id = desig.department.id
            Add_items.designation_id = desig.designation.id
            Add_items.admin_id = A_id
            Add_items.item_status = 'Main'
            Add_items.item_total = int(Add_items.item_qty) * int(Add_items.item_price)
            total = admin_decor_items.objects.filter(
                customer_id=Add_items.customer_id
            )
            stotal = admin_decor_subitems.objects.filter(
                customer_id=Add_items.customer_id
            )
            n=0
            for i in total:
                n+=int(i.item_total or 0)
            s=Add_items.item_total+n 
            p=0
            for q in stotal:
                p+=int(q.sitem_total or 0) 
             
            kk=s+p
            Add_items.item_final_amount = s
            Add_items.item_payable_amount = s - int(advance)
            # Add_items.item_final_amount = a - int(advance)



            Add_items.save()

            Add_items1 = admin_Customer.objects.get(id=Add_items.customer_id)
            Add_items1.customer_payable_amt = kk - int(advance)
            Add_items1.customer_total_amt = kk
            Add_items1.save()
            return render(request,'admin/admin_document.html')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})
    else:
            return redirect('/')

#Add Decor Sub Items Ajax
def admin_ajax_add_subitem(request):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        desig = login_register.objects.get(id=A_id)
        
        if request.method=='POST':
            Add_sitems = admin_decor_subitems()
            Add_sitems.item_category_id = request.POST.get('mscat')
            Add_sitems.item_id = request.POST.get('mitem')
            Add_sitems.subitem = request.POST.get('sitem')
            Add_sitems.sitem_qty = request.POST.get('sqty')
            Add_sitems.sitem_price = request.POST.get('sprice')
            Add_sitems.customer_id = request.POST.get('cid')
            adv = request.POST.get('cadv')
            Add_sitems.branch_id = desig.branch.id
            Add_sitems.department_id = desig.department.id
            Add_sitems.designation_id = desig.designation.id
            Add_sitems.admin_id = A_id
            Add_sitems.sitem_status = 'Sub'
            Add_sitems.sitem_total = int(Add_sitems.sitem_qty) * int(Add_sitems.sitem_price)
            total = admin_decor_subitems.objects.filter(
                customer_id=Add_sitems.customer_id
            )
            mtotal = admin_decor_items.objects.filter(
                customer_id=Add_sitems.customer_id
            )   
            n=0
            for i in total:
                n+=int(i.sitem_total or 0)
            s=Add_sitems.sitem_total+n   
            vv=0 
            for l in mtotal:
                vv+=int(l.item_total or 0)
            
            kk=vv+s
            
            Add_sitems.sitem_final_amount = s
            Add_sitems.sitem_payable_amount = s - int(adv)
            # Add_items.item_final_amount = a - int(advance)



            Add_sitems.save()

            Add_sitems1 = admin_Customer.objects.get(id=Add_sitems.customer_id)
            Add_sitems1.customer_total_amt = kk
            Add_sitems1.customer_payable_amt = kk - int(adv)
            Add_sitems1.save()
            return render(request,'admin/admin_document.html')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})
    else:
            return redirect('/')

#Gallery
def admin_add_gallery(request,id):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        desig = login_register.objects.get(id=A_id)
        view_customer = admin_Customer.objects.get(id=id)

        return render(request,'admin/admin_add_gallery.html',{'cust':view_customer})
        
    else:
            return redirect('/')

#Add Gallery
def admin_ajax_add_gallery_save(request):
    if 'A_id' in request.session:
        if request.session.has_key('A_id'):
            A_id = request.session['A_id']
        else:
            return redirect('/')
        
        desig = login_register.objects.get(id=A_id)
        if request.method=='POST':
            Add_gallery = admin_gallery()
            Add_gallery.img_name = request.POST.get('img_name')
            Add_gallery.gallery_img = request.FILES.get('img')
            Add_gallery.customer_id = request.POST.get('cid')
            Add_gallery.branch_id = desig.branch.id
            Add_gallery.department_id = desig.department.id
            Add_gallery.designation_id = desig.designation.id
            Add_gallery.admin_id = A_id
            
            Add_gallery.save()

            return render(request,'admin/admin_add_gallery.html')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'})
    else:
            return redirect('/')

    