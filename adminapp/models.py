from django.db import models
from homeapp.models import login_register
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

#Decor Items
class admin_Customer(models.Model):
    admin = models.ForeignKey(login_register, on_delete=models.CASCADE,null=True,blank=True)
    customer_name = models.CharField(max_length=300,null=True,blank=True)
    customer_address = models.CharField(max_length=300,null=True,blank=True)
    customer_contact = models.IntegerField(default=1,null=True,blank=True)
    customer_advance = models.IntegerField(default=0,null=True,blank=True)

#Decor Items
class admin_decor_items(models.Model):
    admin = models.ForeignKey(login_register, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(admin_Customer, on_delete=models.CASCADE,null=True,blank=True)
    branch = models.ForeignKey(login_branch, on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey(login_department, on_delete=models.CASCADE,null=True,blank=True)
    designation = models.ForeignKey(login_designation, on_delete=models.CASCADE,null=True,blank=True)
    item_name = models.CharField(max_length=300,null=True,blank=True)
    item_advance = models.IntegerField(default=1,null=True,blank=True)
    item_qty = models.IntegerField(default=1,null=True,blank=True)
    item_price = models.IntegerField(default=1,null=True,blank=True)
    item_total = models.IntegerField(default=1,null=True,blank=True)

    item_final_amount = models.IntegerField(default=0,null=True,blank=True)
    item_status = models.CharField(max_length=300,null=True,blank=True)

#Decor Items
class admin_bill_amount(models.Model):
    admin = models.ForeignKey(login_register, on_delete=models.CASCADE,null=True,blank=True)
    customer = models.ForeignKey(admin_Customer, on_delete=models.CASCADE,null=True,blank=True)
    branch = models.ForeignKey(login_branch, on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey(login_department, on_delete=models.CASCADE,null=True,blank=True)
    designation = models.ForeignKey(login_designation, on_delete=models.CASCADE,null=True,blank=True)

    item_final_amount = models.IntegerField(default=0,null=True,blank=True)
    item_final_status = models.CharField(max_length=300,null=True,blank=True)