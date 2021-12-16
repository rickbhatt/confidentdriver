from celery import shared_task


from django.core.mail import message, send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from datetime import datetime, timedelta


from account.models import CustomUser

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
   


    



