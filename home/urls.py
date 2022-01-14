from django.urls import path

from django.contrib.auth import views as auth_views 

from . import views

urlpatterns=[
    path('',views.home, name='index'),
    path('price', views.price, name='price'),
    path('user', views.user_page, name='user'),
    path('logout', views.logoutUser, name='logout'),
    path('contract', views.contract, name='contract'),
    path('upgrade', views.upgrade, name='upgrade'),
    path('email', views.contract_email, name='email'),
    # path('test-page', views.page, name='test-page'),


]