from datetime import datetime
from celery import shared_task

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from django.utils import timezone

from django.utils.dateparse import parse_datetime


@shared_task
def contract_send_emails(name, user_email, type_of_plan, plan, price, accept, expire):
     # for the customers
                
                accept = parse_datetime(accept)

                expire = parse_datetime(expire)
                
                template = render_to_string('contract_email.html', {'name': name, 'email':user_email, 'type_of_plan':type_of_plan, 'plan': plan,'price': price, 'accept': accept, 'expire': expire})
                email = EmailMessage(
                    'Copy of Contract',                                   #subject
                    template,                                                      # body
                    settings.EMAIL_HOST_USER,
                    [user_email],                                       # sender email
                )
                email.fail_silently = False
                email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                email.send()
                
                #for the owners

                template = render_to_string('contract_email.html', {'name': name, 'email':user_email, 'type_of_plan':type_of_plan, 'plan': plan,'price': price, 'accept': accept, 'expire':expire})
                
                subject = f"Copy of contract for {user_email}"
                
                email = EmailMessage(
                    subject,                                   #subject
                    template,                                                      # body
                    settings.EMAIL_HOST_USER,
                    ['confidentdriver.contract@gmail.com'],                                       # sender email
                )
                email.fail_silently = False
                email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                email.send()

                return "sent"

@shared_task
def updated_contract_send_emails(name, user_email, type_of_plan, plan, price, accept, expire):
    # for the customers
                
                accept = parse_datetime(accept)

                expire = parse_datetime(expire)
                
                template = render_to_string('contract_email.html', {'name': name, 'email':user_email, 'type_of_plan':type_of_plan, 'plan': plan,'price': price, 'accept': accept, 'expire':expire})
                email = EmailMessage(
                    'Copy Updated of Contract',                                   #subject
                    template,                                                      # body
                    settings.EMAIL_HOST_USER,
                    [user_email],                                       # sender email
                )
                email.fail_silently = False
                email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                email.send()
                
                #for the owners

                template = render_to_string('contract_email.html', {'name': name, 'email':user_email, 'type_of_plan':type_of_plan, 'plan': plan,'price': price, 'accept': accept, 'expire':expire})
                
                subject = f"Copy of updated contract for {user_email}"

                
                email = EmailMessage(
                    subject,                                   #subject
                    template,                                                      # body
                    settings.EMAIL_HOST_USER,
                    ['confidentdriver.contract@gmail.com'],                                       # sender email
                )
                email.fail_silently = False
                email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                email.send()

                return "sent"

@shared_task
def customer_query_email(name, cust_email, phone_no, question, asked_on):

    asked_on = parse_datetime(asked_on)
    
    template = render_to_string('customer_query.html', {'name': name, 'email':cust_email, 'phone_no': phone_no,'question': question, 'asked_on': asked_on})
    
    subject = f"Recieved customer query from {cust_email}"

    email = EmailMessage(
        subject,                                   #subject
        template, # body
        settings.EMAIL_HOST_USER,      # sender email
        ['confidentdrivercustomercare@gmail.com'],                # reciever email
    )
    email.fail_silently = False
    email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
    email.send()

    return "sent"



    
    