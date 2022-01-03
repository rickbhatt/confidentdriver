from celery import shared_task


from django.core.mail import message, send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from datetime import datetime, timedelta

from . models import VisitorCount

from account.models import CustomUser, ForgetPassword

from home.models import Contract


@shared_task(bind=True)
def send_expiry_mail(self):

    
     
        users = Contract.objects.all().filter(date_of_expiration__contains = datetime.today().date())

        for user in users:

            # print('\n users', user.user,' and their expiry status is ', user.contract_expired)

            user.contract_expired = True

            user.save()

            # print('\n users after expiring ', user.user,' and their expiry status is now changed to ', user.contract_expired, ' and saved')

            to_email = user.user.email 

            name = user.user.full_name 

            # print('\n sending mail to ', to_email)      

            template = render_to_string('expiry_email.html',{'name':name,})
            email = EmailMessage(
                'Contract Expiration',                                   #subject
                template,                                                      # body
                settings.EMAIL_HOST_USER,
                [to_email],                                       # sender email
            )
            email.fail_silently = False
            email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            email.send()
   

@shared_task
def visitor_count(ip):

    visitor = VisitorCount()

    visitor.ip = ip
    visitor.date_of_record = datetime.now()

    if VisitorCount.objects.all().filter(ip = visitor.ip ,date_of_record__icontains= datetime.today().date()).exists():
        pass
        print("the ip", visitor.ip,"recorded on", visitor.date_of_record ,"already exists and wil not be saved")
    else:
        print('this is the ip address of the user that has been saved', visitor.ip)

        visitor.save()
    return "saved"

@shared_task(bind = True)
def auto_del_forget_password(self):

    fp = ForgetPassword.objects.all()

    for fp_obj in fp:

        fp_obj.delete()
    
    return "Done Deletion"



