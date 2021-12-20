from django.shortcuts import render, redirect

from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control


from .models import Contract, Upgrade, CustomerQuery

from account.models import CustomUser

from .decorators import IfAuthenticatedUser

from datetime import datetime, timedelta

from django.http import HttpResponse

from django.contrib import messages


from .tasks import *

from control.tasks import *

from control.models import VisitorCount

# FOR EMAIL #
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# END FOR EMAIL #

def get_ip(request):

    try:
        ip_forward = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_forward:
            ip = ip_forward.split(",")[0]
            print("returning forwarded for ip address", ip)

        elif request.META.get('HTTP_X_REAL_IP'):
            ip = request.META.get('HTTP_X_REAL_IP')
            print ("returning REAL_IP ", ip)

        else:
            ip = request.META.get('REMOTE_ADDR')
            print("returning remote address ", ip)

    except:
        ip= ""
    
    return ip

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@IfAuthenticatedUser
def home(request):

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_no = request.POST['phone']
        question = request.POST['question']
        asked_on = datetime.now()

        customer_query = CustomerQuery(name=name, email=email, phone_no=phone_no, question=question, asked_on=asked_on)
        customer_query.save()
        
        messages.success(request, 'Your query was sent successfuly.')

        return redirect('/')

    else:
     
        ip = get_ip(request)
        visitor_count.delay(ip)
        
        return render(request, 'index.html')


def price(request):

    return render(request, 'price.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def user_page(request):

    return render(request, 'user.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):                                    # FOR LOGOUT
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    else:
        logout(request)
        return redirect('/')

def contract_email(request):
    return render(request, 'contract_email.html')

@login_required(login_url='login')
def contract(request):

    if request.method == 'POST':
           agreement = Contract()
           

                # for celery
           if request.user.plan == '7days':
                agreement.user = request.user
                agreement.contract_status = True
                expiry = datetime.now() + timedelta(days=7) #days=7
                agreement.date_of_acceptance = datetime.now()
                agreement.date_of_expiration = expiry
                agreement.save()

                name = request.user.full_name
                plan = request.user.plan
                price = 2000
                user_email = request.user.email
                accept = request.user.contract.date_of_acceptance
                expire = request.user.contract.date_of_expiration
                

                contract_send_emails.delay(name, user_email, plan, price, accept, expire)  # in task.py

                # send_emails.delay()
                # # for the customers
                # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': request.user.plan,'price': 2000, 'accept': agreement.date_of_acceptance, 'expire':agreement.date_of_expiration})
                # email = EmailMessage(
                #     'Copy of Contract',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     [request.user.email],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()

                # #for the owners

                # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': request.user.plan,'price': 2000, 'accept': agreement.date_of_acceptance, 'expire':agreement.date_of_expiration})
                # email = EmailMessage(
                #     'Copy of Customer Contract',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     ['confidentdriver.contract@gmail.com'],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()

                return redirect('user')
           

                # for celery
           elif request.user.plan == '14days':   
               agreement.user = request.user
               agreement.contract_status = True
               expiry = datetime.now() + timedelta(days=14) #days=14
               agreement.date_of_acceptance = datetime.now()
               agreement.date_of_expiration = expiry
               agreement.save()

               name = request.user.full_name
               plan = request.user.plan
               price = 3500
               user_email = request.user.email
               accept = request.user.contract.date_of_acceptance
               expire = request.user.contract.date_of_expiration
                
               contract_send_emails.delay(name, user_email, plan, price, accept, expire) #in task.py
               
            #    # for the customers 
            #    template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': request.user.plan,'price': 3500, 'accept': agreement.date_of_acceptance, 'expire':agreement.date_of_expiration})
            #    email = EmailMessage(
            #         'Copy of Contract',                                   #subject
            #         template,                                                      # body
            #         settings.EMAIL_HOST_USER,
            #         [request.user.email],                                       # sender email
            #     )
            #    email.fail_silently = False
            #    email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            #    email.send()

            #    #for the owners

            #    template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': request.user.plan,'price': 3500, 'accept': agreement.date_of_acceptance, 'expire':agreement.date_of_expiration})
            #    email = EmailMessage(
            #         'Copy of Customer Contract',                                   #subject
            #         template,                                                      # body
            #         settings.EMAIL_HOST_USER,
            #         ['confidentdriver.contract@gmail.com'],                                       # sender email
            #     )
            #    email.fail_silently = False
            #    email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            #    email.send()
               
               return redirect('user')
            
           else:
                agreement.user = request.user
                agreement.contract_status = True
                expiry = datetime.now() + timedelta(days=30) #days=30
                agreement.date_of_acceptance = datetime.now()
                agreement.date_of_expiration = expiry
                agreement.save()

                # for celery

                name = request.user.full_name
                plan = request.user.plan
                price = 5000
                user_email = request.user.email
                accept = request.user.contract.date_of_acceptance
                expire = request.user.contract.date_of_expiration

                contract_send_emails.delay(name, user_email, plan, price, accept, expire)  # in task.py
                
                # # for the customers
                # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': request.user.plan,'price': 5000,'accept':agreement.date_of_acceptance, 'expire':agreement.date_of_expiration})
                # email = EmailMessage(
                #     'Copy of Contract',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     [request.user.email],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()

                # #for the owners

                # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': request.user.plan,'price': 5000, 'accept': agreement.date_of_acceptance, 'expire':agreement.date_of_expiration})
                # email = EmailMessage(
                #     'Copy of Customer Contract',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     ['confidentdriver.contract@gmail.com'],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()

                return redirect('user')

    else:
        return render(request, 'contract.html')

@login_required(login_url='login')
def upgrade(request):
   
    if request.method == 'POST':

        user = request.user
        upgraded_to = request.POST['plan']
        initial_plan = request.user.plan
        date_of_upgradation = datetime.now()
                
        upgrade_details = Upgrade(user = user, initial_plan = initial_plan ,upgraded_to = upgraded_to, date_of_upgradation = date_of_upgradation)

        upgrade_details.save()

        # getting objects
        current_user = CustomUser.objects.get(email = request.user)

        current_date = Contract.objects.get(user = request.user)
        
        # setting new expiration dates
        if current_user.plan == '7days':
            if upgraded_to == '14days':
                current_date.date_of_expiration = current_date. date_of_expiration + timedelta(days=7) #days=7
                current_date.save()
            else:
                current_date.date_of_expiration = current_date. date_of_expiration + timedelta(days=23) #days=23
                current_date.save()
        
        elif current_user.plan == '14days':

            current_date.date_of_expiration = current_date.date_of_expiration + timedelta(days=16) #days=16
            current_date.save()
        
        else:
            return HttpResponse('Invalid request')                       

        # upgrading the current plan in Contract() to the upgraded plan  
        current_user.plan = upgraded_to
        current_user.save()    

        # for the customers
        
        if current_user.plan == '14days':

            name = request.user.full_name
            plan = current_user.plan
            price = 3500
            user_email = request.user.email
            accept = current_date.date_of_acceptance
            expire = current_date.date_of_expiration
        
            updated_contract_send_emails.delay(name, user_email, plan, price, accept, expire)  # in task.py

            return render('user')
                
            # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': current_user.plan,'price': 3500, 'accept': current_date.date_of_acceptance, 'expire':current_date.date_of_expiration})
            # email = EmailMessage(
            #     'Copy of Updated Contract',                                   #subject
            #     template,                                                      # body
            #     settings.EMAIL_HOST_USER,
            #     [request.user.email],                                       # sender email
            # )
            # email.fail_silently = False
            # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            # email.send()
        
            # #for the owners
            # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': current_user.plan,'price': 3500, 'accept': current_date.date_of_acceptance, 'expire':current_date.date_of_expiration})
            # email = EmailMessage(
            #     'Copy of Updated Customer Contract',                                   #subject
            #     template,                                                      # body
            #     settings.EMAIL_HOST_USER,
            #     ['confidentdriver.contract@gmail.com'],                                       # sender email
            # )
            # email.fail_silently = False
            # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            # email.send()
        else:

            name = request.user.full_name
            plan = current_user.plan
            price = 5000
            user_email = request.user.email
            accept = current_date.date_of_acceptance
            expire = current_date.date_of_expiration
        
            updated_contract_send_emails.delay(name, user_email, plan, price, accept, expire)  # in task.py

            
            
            # # for the customers
            # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': current_user.plan,'price': 5000, 'accept': current_date.date_of_acceptance, 'expire':current_date.date_of_expiration})
            # email = EmailMessage(
            # 'Copy of Updated Contract',                                   #subject
            # template,                                                      # body
            # settings.EMAIL_HOST_USER,
            # [request.user.email],                                       # sender email
            # )
            # email.fail_silently = False
            # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            # email.send()

            # #for the owners
            # template = render_to_string('contract_email.html', {'name': request.user.full_name, 'email': request.user.email, 'plan': current_user.plan,'price': 5000, 'accept': current_date.date_of_acceptance, 'expire':current_date.date_of_expiration})
            # email = EmailMessage(
            #     'Copy of Updated Customer Contract',                                   #subject
            #     template,                                                      # body
            #     settings.EMAIL_HOST_USER,
            #     ['confidentdriver.contract@gmail.com'],                                       # sender email
            # )
            # email.fail_silently = False
            # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
            # email.send()


            return redirect('user')
    else:
        return render(request, 'upgrade.html')