from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from homeapp.views import *

urlpatterns = [

    #Admin Logout Page
    re_path( r'^Admin_logout/$', views.Admin_logout, name='Admin_logout'),

    #Add Branch Page
    re_path( r'^branch/$', views.admin_branch, name='admin_branch'),

    #Add department Page
    re_path( r'^department/$', views.admin_department, name='admin_department'),

    #Add designation Page
    re_path( r'^designation/$', views.admin_designation, name='admin_designation'),

    #Display Dashboard Page
    re_path(r'^$', views.admin_dashboard, name='admin_dashboard'),

    #Add Document, list Document Page
    re_path(r'^admin_view_document/$', views.admin_view_document, name='admin_view_document'),

    #View Document Page
    re_path( r'^admin_view_pdf/$', views.admin_view_pdf, name='admin_view_pdf'),

    #Add Decor Items
    re_path( r'^admin_ajax_add_quotation/$', views.admin_ajax_add_quotation, name='admin_ajax_add_quotation'),
    
    
    
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
