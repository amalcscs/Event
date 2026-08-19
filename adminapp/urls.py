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
    re_path(r'^admin_view_list/$', views.admin_view_list, name='admin_view_list'),

    #View Document Page
    re_path( r'^admin_view_pdf/$', views.admin_view_pdf, name='admin_view_pdf'),

    #Add Document Page
    re_path( r'^admin_document/(?P<id>\d+)$', views.admin_document, name='admin_document'),

    #Add Customer
    re_path( r'^admin_ajax_add_customer/$', views.admin_ajax_add_customer, name='admin_ajax_add_customer'),

    #Add Decor Items
    re_path( r'^admin_ajax_add_quotation/$', views.admin_ajax_add_quotation, name='admin_ajax_add_quotation'),

    #Add Advance And Form Submit
    re_path( r'^admin_add_AdvanceAndFormSubmit/$', views.admin_add_AdvanceAndFormSubmit, name='admin_add_AdvanceAndFormSubmit'),
    
    
    
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
