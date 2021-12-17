from django.contrib import admin

from .models import CustomerPaymentDetail

@admin.register(CustomerPaymentDetail)
class ContractAdmin(admin.ModelAdmin):
   list_display = ('user', 'customer_plan', 'fees_taken', 'transaction_id', 'date_of_payment', 'paid')
   ordering= ('-date_of_payment',)
   search_fields= ('user', 'date_of_payment', 'transaction_id')