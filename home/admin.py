from django.contrib import admin
from django.db import models
from .models import Contract, Upgrade, CustomerQuery
# Register your models here.

@admin.register(CustomerQuery)
class ContractAdmin(admin.ModelAdmin):
    list_display= ('name', 'email','phone_no', 'question', 'asked_on')
    ordering=('-asked_on',)
    search_fields=('email', 'phone_no', 'name')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display= ('user', 'contract_status', 'contract_expired','date_of_acceptance', 'date_of_expiration')
    ordering=('-date_of_expiration',)
    search_fields=('user', 'date_of_acceptance', 'date_of_expiration')

@admin.register(Upgrade)
class UpgradeAdmin(admin.ModelAdmin):
    list_display= ('user', 'initial_plan' , 'upgraded_to','date_of_upgradation')
    ordering=('-date_of_upgradation',)
    search_fields=('user','date_of_upgradation')