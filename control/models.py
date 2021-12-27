from django.db import models
from django.db.models.base import Model

from account.models import CustomUser

# Create your models here.

class CustomerPaymentDetail(models.Model):

    user_email = models.EmailField(max_length=255, null =True)
    customer_plan = models.CharField(max_length=7, null=True)
    fees_taken = models.IntegerField(null= True)
    transaction_id = models.CharField(max_length=255, null= True)
    date_of_payment = models.DateTimeField(null= True)
    paid = models.BooleanField(default= False)


class VisitorCount(models.Model):

    ip = models.TextField(null=True)
    date_of_record = models.DateTimeField(null=True)