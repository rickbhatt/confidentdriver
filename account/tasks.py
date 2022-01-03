from celery import shared_task

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

import uuid

from django.utils.dateparse import parse_datetime



@shared_task
def regd_send_email(name, phone, address, type_of_plan,plan, user_email):

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
            template = render_to_string('hire.html', {'name': name, 'phone': phone, 'address': address,'type_of_plan': type_of_plan,'plan': plan, 'email': user_email})
            
            subject = f"New registration for {user_email} contact customer"
            
            email = EmailMessage(
                subject,                                   #subject
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
@shared_task
def forget_password_mail(user_email, name, token):
    
    subject = "Forget Password Link"

    message = f"Hello, {name} \n Click the link to reset your password \n http://127.0.0.1:8000/account/change-password/{token}"

    email_from = settings.EMAIL_HOST_USER

    reciepent_list = [user_email]

    send_mail(subject, message, email_from, reciepent_list, fail_silently= False)

    return True

@shared_task
def send_to_developer(path, date_of_record, error):
    
    date_of_record = parse_datetime(date_of_record)
    
    message = f"this exception/ error is generated from confident driver and the source of error is : {path}, and the error/ exception is : {error}"
    
    subject = f"this error is from confident driver, {date_of_record}"

    email = EmailMessage(
        subject,                                   #subject
        message,                                                      # body
        settings.EMAIL_HOST_USER,
        ['error.reports.ritankar@gmail.com'],                                       # sender email
    )
    email.fail_silently = False
    email.send()

    return "sent"