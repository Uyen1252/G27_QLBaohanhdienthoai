from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
       
class Phone(models.Model):
    serial = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    NCC = models.CharField(max_length=255)
    description = models.TextField(null=True, max_length=255)
    
    def __str__(self):
        return self.serial
    
    def is_under_warranty(self):
        return self.end_date >= date.today()

    def warranty_status(self):
        if self.is_under_warranty():
            return "Còn hạn bảo hành"
        else:
            return "Hết hạn bảo hành"

    
class Warranty(models.Model):
    MKH = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    NCC = models.CharField(max_length=255)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.MKH
