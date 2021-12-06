from django.urls import path



from django.contrib.auth import views as auth_views 

from . import views

from .views import resend_otp

urlpatterns=[
    path('register',views.registerpage, name='register'),
    path('login',views.loginpage, name='login'),

    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name="password_reset.html"), 
    name="reset_password"),                                                                                            #submit email form
    
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
    name="password_reset_done"),               #email sent success message
    
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
    name="password_reset_confirm"),         # link to password reset form in email
    
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
    name="password_reset_complete"),       # password succesfully changed message

    path('resendOTP', resend_otp)


]