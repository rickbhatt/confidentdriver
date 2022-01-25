from datetime import date, datetime
from django.shortcuts import render, redirect 
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model

from control.views import dashboard

from home.views import get_ip, visitor_count

from django.views.decorators.cache import cache_control

import uuid

#################### celery queing ############################

from .tasks import *

################# end of celery queing ######################

##################### CUSTOM USER MODEL ###########################

from .models import CustomUser, ForgetPassword

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
                type_of_plan = user.type_of_plan
                plan = user.plan
                user_email= user.email

                regd_send_email.delay(name, phone, address, type_of_plan, plan, user_email)

              
                messages.success(request,'Your account has been created successfully.')
                return redirect('login')
            else:
                messages.error(request, 'OTP entered is wrong')
                return render(request, 'register.html', {'otp': True, 'user': user})

        
        full_name = request.POST.get('full_name')
        age = request.POST.get('age')
        phone_no = request.POST.get('phone')
        address = request.POST.get('address')
        type_of_plan = request.POST.get('type_of_plan')
        plan = request.POST.get('plan')
        email = request.POST.get('email')
        password1= request.POST.get('password')
        password2= request.POST.get('con_password')

        if password1==password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'User with same email already exists')
                return redirect('register')
            
            elif int(age) < 18:
                messages.info(request, 'You have to be above 18 to register')
                return redirect('register') 
            
            elif type_of_plan is None:
                messages.info(request, 'Please select type of plan')
                return redirect('register') 
            
            elif plan is None:
                messages.info(request, 'Please select a plan')
                return redirect('register') 
            else:
                user=CustomUser.objects.create_user(full_name=full_name.upper(),age=age, phone_no=phone_no, address=address,  type_of_plan= type_of_plan,plan=plan, email=email.lower(), password=password1)
                user.is_active = False
                user.save()
                
                usr_otp = random.randint(100000, 999999)
                UserOtp.objects.create(user = user, otp = usr_otp)
                
                name= user.full_name
                usr_otp = usr_otp
                user_email = user.email
                
                otp_send_mail.delay(name, usr_otp, user_email)


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
                type_of_plan = user.type_of_plan
                plan = user.plan
                user_email= user.email

                regd_send_email.delay(name, phone, address, type_of_plan, plan, user_email)
                
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
            return render(request, 'login.html', {'otp': True, 'user': user})
        
        else:
            messages.warning(request, 'UserID or Password is incorrect!')
            return render( request, 'login.html')            #FOR ERROR PURPOSE

    else:

        ip = get_ip(request)
        visitor_count(ip)

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

#################### PASSWORD RESET CHANGE ######################

def change_password(request, token):

    try:
        fp_obj = ForgetPassword.objects.filter(forget_password_token = token).first()

        print("\nthis is user obj ", fp_obj.user, "\n")

        if request.method == 'POST':
            new_password = request.POST.get('password')
            con_password = request.POST.get('con_password')
            user_id = request.POST.get('user')

            if user_id is None:
                messages.info(request, 'User does not exist.')
                return redirect(request.path_info)
            else:
                if new_password != con_password:
                    messages.info(request, 'Password and Confirm Password not matching')
                    return redirect(request.path_info)
                else:
                    user_obj = CustomUser.objects.get(email = user_id)
                    user_obj.set_password(new_password)
                    user_obj.save()

                    messages.info(request, 'Password changed successfuly')

                    return redirect('login')


        context = {'user': fp_obj.user}

    except Exception as e:

        path = "account/views/change_password()"

        date_of_record = datetime.now()

        error = str(e)
        
        send_to_developer.delay(path, date_of_record, error)
        print("\nthe exception is comming from forget_password : ", e, "\n")
        messages.info(request, 'We are facing some problem. We shall rectify it soon. Sorry for inconvenience caused.')

        print("this is the exception from chamge_password : ", e)
        return redirect(request.path_info)

    return render(request, 'change_password.html', context)

def forget_password(request):

    try:

        if request.method == 'POST':
            user_email = request.POST.get('email')

            if CustomUser.objects.filter(email = user_email).exists():
                
                user_obj = CustomUser.objects.get(email = user_email)

                name = user_obj.full_name
                plan = user_obj.plan

                print("\n this is the user : ", user_obj, " this is its name : ", name,"\n")

                token = str(uuid.uuid4())
                
                fp = ForgetPassword.objects.get_or_create(user = user_obj, forget_password_token = token)

                forget_password_mail.delay(user_email, name, token)
                messages.info(request, f'An email has been sent to {user_obj}.')
                return redirect('forget-password')  
            else:
                messages.info(request, 'User does not exist')
                return redirect('forget-password')   

    except Exception as e:

        path = "account/views/forget_password()"

        date_of_record = datetime.now()

        error = str(e)
        
        send_to_developer.delay(path, date_of_record, error)
        print("\nthe exception is comming from forget_password : ", e, "\n")
        messages.info(request, 'We are facing some problem. We shall rectify it soon. Sorry for inconvenience caused.')
        return redirect('forget-password')  
    
    return render(request, 'fp_email_form.html')

#################### END PASSWORD RESET CHANGE ######################
