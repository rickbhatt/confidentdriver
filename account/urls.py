from django.urls import path



from django.contrib.auth import views as auth_views 

from . import views

from .views import resend_otp

urlpatterns=[
    path('register',views.registerpage, name='register'),
    path('login',views.loginpage, name='login'),

    path('forget-password',views.forget_password, name='forget-password'),
    
    path('change-password/<token>/',views.change_password, name='change-password'),

    path('resendOTP', resend_otp)


]