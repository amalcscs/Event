from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    #Dashboard
    re_path(r'^$', views.admin_dashboard, name='admin_dashboard'),

    #Document
    re_path(r'^admin_view_document/$', views.admin_view_document, name='admin_view_document'),
    re_path( r'^admin_view_pdf/$', views.admin_view_pdf, name='admin_view_pdf'),
    
    
    
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
