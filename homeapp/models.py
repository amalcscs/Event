from django.db import models
from adminapp.models import *
# Create your models here.
#Register

class login_register(models.Model):
    branch = models.ForeignKey(login_branch, on_delete=models.CASCADE,null=True, blank=True)
    department = models.ForeignKey(login_department, on_delete=models.CASCADE,null=True,blank=True)
    designation = models.ForeignKey(login_designation, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    profile_pic = models.FileField(upload_to = 'home/gallery/profile_images/')