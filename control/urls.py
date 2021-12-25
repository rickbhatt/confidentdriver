from django.urls import path

from . import views


urlpatterns=[
    path('dashboard',views.dashboard, name='dashboard'),
    path('analytics',views.analytics, name='analytics'),
    path('user-list',views.user_list, name='user-list'),
    path('contract-list',views.contract_list, name='contract-list'),
    path('staff-list',views.staff_list, name='staff-list'),
    path('payments-form',views.payments_form, name='payments-form'),

    
    ############### for ajax calls #########################
    path('visitor-data',views.visitor_data, name='visitor-data'),
    path('user-data',views.user_data, name='user-data'),




]