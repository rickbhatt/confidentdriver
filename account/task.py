from celery import shared_task

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string



@shared_task
def regd_send_email(name, phone, address, plan, user_email):

    # to the customer
            template = render_to_string('regd_success_email.html', {'name': name})
            email = EmailMessage(
                'Registration Successfull',                                   #subject
                template,                                                      # body
                settings.EMAIL_HOST_USER,
                [user_email],                                       # sender email
            )
            email.fail_silently = False
            email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            email.send()

            
            # to the owners
            template = render_to_string('hire.html', {'name': name, 'phone': phone, 'address': address, 'plan': plan, 'email': user_email})
            email = EmailMessage(
                'New regsitration contact customer',                                   #subject
                template,                                                      # body
                settings.EMAIL_HOST_USER,
                ['confidentdriver.owner@gmail.com'],                                       # sender email
            )
            email.fail_silently = False
            email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            email.send()

            return None

@shared_task
def otp_send_mail(name, usr_otp, user_email):
    
       mess =  f"Hello, {name},\n Please enter the otp to validate your email and activate your account. \nYour OTP is {usr_otp} .\n Thanks!"
                
       send_mail(
            "Welcome to Confident Driver - Verify your Email",   #subject
            mess,  #message
            settings.EMAIL_HOST_USER,  # sender
            [user_email],           #reciever
            fail_silently= False
        )
