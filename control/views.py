from django.shortcuts import render, redirect

from django.http import JsonResponse

from datetime import datetime, date

from django.contrib import messages

from . models import CustomerPaymentDetail, VisitorCount

from home.models import *

from account.models import *

from .tasks import *

from .decorators import OnlySuperuser

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control

from django.db.models.functions import ExtractMonth, ExtractYear

from django.db.models import Count, F, Func, Value, CharField

from django.http import JsonResponse

####################### DASHBOARD ############################


# def nav(request):

#     return render(request, 'control_nav_bar.html')`


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def dashboard(request):

    today = datetime.today()

    currentYear = datetime.now()
    
    all_users = CustomUser.objects.all().filter(is_active = True).exclude(is_staff = True).exclude(is_active = False).count()
    
    all_users_bydate = CustomUser.objects.all().filter(date_joined__contains= datetime.today().date()).exclude(is_staff = True).exclude(is_active = False).count()

    current_month_user = CustomUser.objects.all().filter(date_joined__month = today.month, date_joined__year = currentYear.year).exclude(is_staff = True).exclude(is_active = False).exclude(is_staff = True).count()

    all_contracts = Contract.objects.all().count()

    contract_signed_today = Contract.objects.all().filter(date_of_acceptance__contains= datetime.today().date()).count()

    contract_expire_today  = Contract.objects.all().filter(date_of_expiration__contains= datetime.today().date()).count()

    total_visitors = VisitorCount.objects.all().count()
    
    visitor_today = VisitorCount.objects.all().filter(date_of_record__icontains = datetime.today().date()).count()

    current_month_visitor = VisitorCount.objects.all().filter(date_of_record__month = today.month, date_of_record__year=currentYear.year).count()

    current_year_visitor = VisitorCount.objects.all().filter(date_of_record__year = today.year).count()


    context = {
    'all_users': all_users,
    'current_month_user': current_month_user, 
    'all_users_bydate':all_users_bydate,
    'all_contracts':all_contracts ,'contract_signed_today':contract_signed_today,
    'contract_expire_today': contract_expire_today, 'total_visitors':total_visitors ,
    'visitor_today': visitor_today,
    'current_month_visitor': current_month_visitor,
    'current_year_visitor': current_year_visitor
    }

    return render(request, 'dashboard.html', context)

####################### ANALYTICS ############################
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def analytics(request):

    return render(request, "chart.html")

####################### USERS LIST ############################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def user_list(request):

    userList = CustomUser.objects.all().exclude(is_staff = True).order_by('date_joined')

    userListCount = CustomUser.objects.all().exclude(is_staff = True).count()
    
    context = {'userList': userList,
                'userListCount': userListCount}

    return render(request, "user_list.html", context)

####################### USER CONTRACT LIST ############################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def contract_list(request):

    contractList = Contract.objects.all().order_by('date_of_acceptance')

    context = {'contractList': contractList}
    
    return render(request, "contract_list.html", context)

####################### STAFF LIST ############################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def staff_list(request):

    staffList = CustomUser.objects.filter(is_staff = True).order_by('date_joined')

    staffListCount = CustomUser.objects.filter(is_staff = True).count()

    context = {'staffList': staffList,
                'staffListCount': staffListCount}
    
    return render(request, "staff_list.html", context)

####################### PAYMENTS FORM ############################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def payments_form(request):

    if request.method == 'POST':

        user_email = request.POST.get('user_email')
        transaction_id = request.POST.get('trasaction_id')
        
        if CustomUser.objects.filter(email = user_email).exists():

            user = CustomUser.objects.get(email = user_email)
            user_email = user
            customer_plan = user.plan
            if user.plan == "7days":
                fees_taken = 2000
            elif user.plan == "14days":
                fees_taken = 3500
            else:
                fees_taken = 5000
            
            date_of_payment = user.contract.date_of_expiration
            paid = True

            cust_payment = CustomerPaymentDetail(user_email = user_email, customer_plan=customer_plan, fees_taken=fees_taken, transaction_id=transaction_id, date_of_payment=date_of_payment, paid=paid)

            cust_payment.save()

            messages.info(request, 'Details Uploaded')
            return redirect('payments-form') 

        else:
            messages.info(request, 'The user email entered does not exist')
            return render( request, 'payments_form.html') 
    
    else:
        payments = CustomerPaymentDetail.objects.all().order_by('date_of_payment')

        context = {'payments': payments}

        return render(request, "payments_form.html", context)



################## FOR AJAX CALLS ##############################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def visitor_data(request):  # for visirtors
    
    currentYear = datetime.now()
    
    visitorMonthNumber = []
    visitorNumberMonthly = []

    vistorYearNumber =[]
    visitorNumberYearly = []

    monthly_visitor = VisitorCount.objects.all().filter(
    date_of_record__year=currentYear.year
        ).values(
            'date_of_record__month'
        ).annotate(
            total_in_month=Count('ip'),
            formatted_date=Func(
                F('date_of_record'),
                Value('MONTH'),
                function='to_char',
                output_field=CharField()
            )
        ).order_by('date_of_record__month')
    
    print("\n", monthly_visitor, "\n")
    
    yearly_visitor = VisitorCount.objects.all().values('date_of_record__year').annotate(
        total_in_year= Count('ip')
        ).order_by('date_of_record__year')

    for i in range(len(monthly_visitor)):

        visitorMonthNumber.append(monthly_visitor[i]['formatted_date'])
        visitorNumberMonthly.append(monthly_visitor[i]['total_in_month']) 
    
    print("\nthis is the list of month number =", visitorMonthNumber, "\n", "\nthis is the number of visitors", visitorNumberMonthly, "\n")
    

    for j in range(len(yearly_visitor)):
        
        vistorYearNumber.append(yearly_visitor[j]['date_of_record__year'])
        visitorNumberYearly.append(yearly_visitor[j]['total_in_year']) 
   
    print("In the year :",yearly_visitor[j]['date_of_record__year'],"-", " the number of visitors are :", yearly_visitor[j]['total_in_year'] ,"\n")

    visitor_stats = {
            "visitorMonthNumber": visitorMonthNumber,
            "visitorNumberMonthly":  visitorNumberMonthly,
            "vistorYearNumber": vistorYearNumber,
            "visitorNumberYearly": visitorNumberYearly,

    }

    return JsonResponse(visitor_stats)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def user_data(request):  #for users

    currentYear = datetime.now()

    
    userspermonth = []
    usersmonthnumber =[]

    usersperyear =[]
    usersyearnumber = []
    
    monthly_users = CustomUser.objects.all().filter(date_joined__year = currentYear.year).values(
    'date_joined__month'
    ).exclude(is_staff = True).exclude(is_active=False).annotate(
        total_in_month=Count('email'),
        formatted_date=Func(
                F('date_joined'),
                Value('MONTH'),
                function='to_char',
                output_field=CharField()
            ) 
        ).order_by('date_joined__month')

    yearly_users = CustomUser.objects.all().values('date_joined__year').exclude(is_staff = True).exclude(is_active =False).annotate(
        total_in_year= Count('email')
        ).order_by('date_joined__year')

    for i in range(len(monthly_users)):

        usersmonthnumber.append(monthly_users[i]['formatted_date'])
        userspermonth.append(monthly_users[i]['total_in_month']) 
    
    for j in range(len( yearly_users)):
        
        usersyearnumber.append( yearly_users[j]['date_joined__year'])
        usersperyear.append( yearly_users[j]['total_in_year']) 
    
    
    print("\n" ,usersyearnumber, userspermonth, "\n")

    user_stats = {
            "usersmonthnumber": usersmonthnumber,
            "userspermonth":  userspermonth,
            "usersyearnumber": usersyearnumber,
            "usersperyear":  usersperyear,

    }

    return JsonResponse(user_stats)
    