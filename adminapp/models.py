from django.db import models

# Create your models here.

#Branch
class login_branch(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    profile_pic = models.FileField(upload_to = 'admin/gallery/branch_images/')

#Department
class login_department(models.Model):
    branch = models.ForeignKey(login_branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)

#Designation
class login_designation(models.Model):
    branch = models.ForeignKey(login_branch, on_delete=models.CASCADE)
    department = models.ForeignKey(login_department, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    profile_pic = models.FileField(upload_to = 'admin/gallery/designation_images/')