from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
       
class Phone(models.Model):
    serial = models.IntegerField()
    name = models.CharField(max_length=50)
    name_brand = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    NCC = models.CharField(max_length=50)
    description = models.TextField(null=True, max_length=100)
    
    def __str__(self):
        return f"{self.serial}"
    
    
    def is_under_warranty(self):
        return self.end_date >= date.today()

    def warranty_status(self):
        if self.is_under_warranty():
            return "Còn hạn bảo hành"
        else:
            return "Hết hạn bảo hành"

    
class Warranty(models.Model):
    id = models.IntegerField(primary_key=True)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    MGD = models.CharField(max_length=10, unique=True)
    name_KH = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30)
    ngaynhan = models.DateField()
    ngaytra = models.DateField()
    note = models.TextField(null=True)

    def __str__(self):
        return self.MGD
    
    

    
