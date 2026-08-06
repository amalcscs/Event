from django.shortcuts import render,redirect
from .models import *;
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os


#Dashboard
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

def admin_view_document(request):
    return render(request,'admin/admin_view_document.html')

#Document
def admin_view_pdf(request):

    
    template_path = 'admin/admin_view_pdf.html'
    context = {
    "background": os.path.join(settings.MEDIA_ROOT, "background2.jpg"),
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

