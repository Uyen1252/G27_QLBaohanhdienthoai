from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Phone(models.Model):
    serial = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

        


class Warranty(models.Model):
    serial = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    NCC = models.CharField(max_length=255)
    description = models.TextField(null=True)

    # Set up foreign key to Phone model
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    
    
class Customer(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    NCC = models.CharField(max_length=255)
    description = models.TextField(null=True)
