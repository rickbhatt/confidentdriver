from typing import OrderedDict
from django.contrib import admin

from .models import CustomerPaymentDetail, VisitorCount

@admin.register(CustomerPaymentDetail)
class CustomerPayementDetailtAdmin(admin.ModelAdmin):
   list_display = ('user', 'customer_plan', 'fees_taken', 'transaction_id', 'date_of_payment', 'paid')
   ordering= ('-date_of_payment',)
   search_fields= ('user', 'date_of_payment', 'transaction_id')

@admin.register(VisitorCount)
class VistorAdmin(admin.ModelAdmin):
   list_display = ("ip", "date_of_record")
   ordering = ("-date_of_record",)
   search_fields = ("ip",)