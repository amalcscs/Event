from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    #Home Page
    re_path(r'^$', views.home_index, name='home_index'),

    #Register Page
    re_path( r'^register/$', views.register, name='register'),

    #Login Page
    re_path( r'^login/$', views.login, name='login'),
    
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
