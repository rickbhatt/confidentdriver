from django import template
from django.shortcuts import render, redirect 
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model

from control.views import dashboard

from django.views.decorators.cache import cache_control

#################### celery queing ############################

from .tasks import *

################# end of celery queing ######################

##################### CUSTOM USER MODEL ###########################

from .models import CustomUser

#################### END OF CUSTOM USER MODEL ######################

##################### for otp ###########################

import random
from .models import UserOtp
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
##################### end for otp ###########################

############## FORM VIEWS OF OTHER APPS ##############

from home.views import user_page
from control.views import dashboard
############## END FORM VIEWS OF OTHER APPS ##############


User = get_user_model()

def registerpage(request):

    if request.method == 'POST':
        
        get_otp = request.POST.get('otp')

        if get_otp:
            get_user= request.POST.get('user')
            user = CustomUser.objects.get(email=get_user)
           
            if int(get_otp) == UserOtp.objects.filter(user= user).last().otp:
                user.is_active = True
                user.save()
                
                # for celery
                
                name = user.full_name
                phone = user.phone_no
                address = user.address
                plan = user.plan
                user_email= user.email

                regd_send_email.delay(name, phone, address, plan, user_email)

                # # to the customer
                # template = render_to_string('regd_success_email.html', {'name': user.full_name})
                # email = EmailMessage(
                #     'Registration Successfull',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     [user.email],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()

                
                # # to the owners
                # template = render_to_string('hire.html', {'name': user.full_name, 'phone': user.phone_no, 'address': user.address, 'plan': user.plan, 'email': user.email})
                # email = EmailMessage(
                #     'New regsitration contact customer',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     ['confidentdriver.owner@gmail.com'],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()
                
                messages.success(request,'Your account has been created successfully.')
                return redirect('login')
            else:
                messages.error(request, 'OTP entered is wrong')
                return render(request, 'register.html', {'otp': True, 'user': user})

        
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        phone_no = request.POST.get('phone')
        address = request.POST.get('address')
        plan = request.POST.get('plan')
        email = request.POST.get('email')
        password1= request.POST.get('password')
        password2= request.POST.get('con_password')

        if password1==password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'User with same email already exists')
                return redirect('register')
            
            elif plan is None:
                messages.info(request, 'Please select a plan')
                return redirect('register') 
            else:
                user=CustomUser.objects.create_user(full_name=full_name.upper(),age=age, phone_no=phone_no, address=address, plan=plan, email=email.lower(), password=password1)
                user.is_active = False
                user.save()
                
                usr_otp = random.randint(100000, 999999)
                UserOtp.objects.create(user = user, otp = usr_otp)
                
                name= user.full_name
                usr_otp = usr_otp
                user_email = user.email
                
                otp_send_mail.delay(name, usr_otp, user_email)

                # mess =  f"Hello, {user.full_name},\n Please enter the otp to validate your email and activate your account. \nYour OTP is {usr_otp} .\n Thanks!"
                
                # send_mail(
                #     "Welcome to Confident Driver - Verify your Email",   #subject
                #     mess,  #message
                #     settings.EMAIL_HOST_USER,  # sender
                #     [user.email],           #reciever
                #     fail_silently= False
                # )

                return render(request, 'register.html', {'otp': True, 'user': user})
                # return redirect('login')
        else:
            messages.info(request, 'Password and Confirm Password not matching')
            return redirect('register') 
    else:
        return render(request, 'register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginpage(request):

    # user = get_user_model()

    if request.method == 'POST':
        
        get_otp = request.POST.get('otp')

        if get_otp:
            get_user= request.POST.get('user')
            user = CustomUser.objects.get(email=get_user)
           
            if int(get_otp) == UserOtp.objects.filter(user= user).last().otp:
                user.is_active = True
                user.save()
                
                # for celery
                
                name = user.full_name
                phone = user.phone_no
                address = user.address
                plan = user.plan
                user_email= user.email

                regd_send_email.delay(name, phone, address, plan, user_email)
                
                # #to the customers
                # template = render_to_string('regd_success_email.html', {'name': user.full_name})
                # email = EmailMessage(
                #     'Registration Successfull',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     [user.email],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()


                #  # to the owners
                # template = render_to_string('hire.html', {'name': user.full_name, 'phone': user.phone_no, 'address': user.address, 'plan': user.plan, 'email': user.email})
                # email = EmailMessage(
                #     'New regsitration contact customer',                                   #subject
                #     template,                                                      # body
                #     settings.EMAIL_HOST_USER,
                #     ['confidentdriver.owner@gmail.com'],                                       # sender email
                # )
                # email.fail_silently = False
                # email.content_subtype = 'html'       # WITHOUT THIS THE HTML WILL GET RENDERED AS PLAIN TEXT
                # email.send()
                
                login(request, user)
                return redirect(user_page)
            else:
                messages.error(request, 'OTP entered is wrong')
                return render(request, 'register.html', {'otp': True, 'user': user})
        
        
        # email=request.POST['email']               #this works too
        # password=request.POST['password']

        email =  request.POST.get('email')
        password = request.POST.get('password')

        # user = CustomUser.objects.get(email=username, password=password)
        

        user = authenticate(request, email= email, password= password) #changed username to email because Custom User has no username field

        if user is not None:
            
            if user.is_staff:
                login(request, user)
                return redirect(dashboard) # this is in control views
            else:
                login(request, user)
                return redirect(user_page) # this is in home views
        
        elif not CustomUser.objects.filter(email=email).exists():
            messages.info(request, "No user with this username exists \n You are requested to register first.")
            return render( request, 'login.html')
        elif not CustomUser.objects.get(email=email).is_active:
            user = CustomUser.objects.get(email=email)

            usr_otp = random.randint(100000, 999999)
            UserOtp.objects.create(user = user, otp = usr_otp)
            
            name= user.full_name
            usr_otp = usr_otp
            user_email = user.email
                
            otp_send_mail.delay(name, usr_otp, user_email)
            
            # mess =  f"Hello, {user.full_name},\n Please enter the otp to validate your email and activate your account. \nYour OTP is {usr_otp} .\n Thanks!"
            
            # send_mail(
            #     "Welcome to Confident Driver - Verify your Email",   #subject
            #     mess,  #message
            #     settings.EMAIL_HOST_USER,  # sender
            #     [user.email],           #reciever
            #     fail_silently= False
            # )
            return render(request, 'login.html', {'otp': True, 'user': user})
        
        else:
            messages.info(request, 'UserID or Password is incorrect!')
            return render( request, 'login.html')            #FOR ERROR PURPOSE

    else:
        return render(request, 'login.html')



def t_and_c(request):
    return render(request, 'terms_and_condition.html')



################## RESEND OTP ##################

def resend_otp(request):
    if request.method == 'GET':
        get_usr = request.GET['usr']
        
        if CustomUser.objects.filter(email=get_usr).exists() and not CustomUser.objects.get(email=get_usr).is_active:
            
                usr = CustomUser.objects.get(email=get_usr)
                
                usr_otp = random.randint(100000, 999999)
                UserOtp.objects.create(user = usr, otp = usr_otp)
                mess = f"Hello, {usr.full_name},\n Please enter the otp to validate your email and activate your account. \nYour OTP is {usr_otp} .\n Thanks!"
                
                send_mail(
                        "Welcome to Confident Driver - Verify your Email",   #subject
                        mess,  #message
                        settings.EMAIL_HOST_USER,  # sender
                        [usr.email],           #reciever
                        fail_silently= False
                    )
                return HttpResponse("Resend")

    
    return HttpResponse("Can't Send OTP")

################## END OF RESEND OTP ############