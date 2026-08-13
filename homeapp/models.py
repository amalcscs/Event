from django.db import models
# Create your models here.
#Register

class login_register(models.Model):
    branch = models.ForeignKey('adminapp.login_branch', on_delete=models.CASCADE,null=True, blank=True)
    department = models.ForeignKey('adminapp.login_department', on_delete=models.CASCADE,null=True,blank=True)
    designation = models.ForeignKey('adminapp.login_designation', on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    profile_pic = models.FileField(upload_to = 'home/gallery/profile_images/')