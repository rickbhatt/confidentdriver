from django.db import models
from django.db.models.expressions import F
from account.models import CustomUser
from django.utils import timezone


# Create your models here.


class CustomerQuery(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone_no = models.CharField(max_length=10, null=True)
    question = models.TextField(null=True)
    asked_on = models.DateTimeField(null= True)
      

class Contract(models.Model):
    user = models.OneToOneField(CustomUser, null= True, on_delete=models.CASCADE)
    contract_status = models.BooleanField(default=False)
    date_of_acceptance = models.DateTimeField(null= True)
    date_of_expiration = models.DateTimeField(null=True, blank=True)


class Upgrade(models.Model):
    user = models.OneToOneField(CustomUser, null= True, on_delete=models.CASCADE)
    initial_plan = models.CharField(max_length=6, null= True, blank=True)
    upgraded_to = models.CharField(max_length=6, null= True, blank=True)
    date_of_upgradation = models.DateTimeField(null= True)
