from django.db import models

from account.models import CustomUser

# Create your models here.

class CustomerPaymentDetail(models.Model):

    user = models.OneToOneField(CustomUser, null=True, on_delete= models.CASCADE)
    customer_plan = models.CharField(max_length=7, null=True)
    fees_taken = models.CharField(max_length=4, null= True)
    transaction_id = models.CharField(max_length=255, null= True)
    date_of_payment = models.DateTimeField(null= True)
    paid = models.BooleanField(default= False)