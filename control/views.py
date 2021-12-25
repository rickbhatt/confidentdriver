from django.shortcuts import render, redirect

from django.http import JsonResponse

from datetime import datetime, date

from . models import VisitorCount

from home.models import *

from account.models import *

from .tasks import *

from .decorators import OnlySuperuser

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control

from django.db.models.functions import ExtractMonth, ExtractYear

from django.db.models import Count

from django.http import JsonResponse


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def dashboard(request):

    today = datetime.today()
    
    all_users = CustomUser.objects.all().filter(is_active = True).exclude(is_staff = True).count()
    
    all_users_bydate = CustomUser.objects.all().filter(date_joined__contains= datetime.today().date()).exclude(is_staff = True).count()

    all_contracts = Contract.objects.all().count()

    contract_signed_today = Contract.objects.all().filter(date_of_acceptance__contains= datetime.today().date()).count()

    contract_expire_today  = Contract.objects.all().filter(date_of_expiration__contains= datetime.today().date()).count()

    total_visitors = VisitorCount.objects.all().count()
    
    visitor_today = VisitorCount.objects.all().filter(date_of_record__icontains = datetime.today().date()).count()

    current_month_visitor = VisitorCount.objects.all().filter(date_of_record__month = today.month).count()

    current_year_visitor = VisitorCount.objects.all().filter(date_of_record__year = today.year).count()


    context = {
    'all_users': all_users, 
    'all_users_bydate':all_users_bydate,
    'all_contracts':all_contracts ,'contract_signed_today':contract_signed_today,
    'contract_expire_today': contract_expire_today, 'total_visitors':total_visitors ,
    'visitor_today': visitor_today,
    'current_month_visitor': current_month_visitor,
    'current_year_visitor': current_year_visitor
    }

    return render(request, 'dashboard.html', context)


    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def analytics(request):

    user_data(request)
    
    return render(request, "chart.html")



################## FOR AJAX CALLS ##############################

def visitor_data(request):  # for visirtors
    
    visitorMonthNumber = []
    visitorNumberMonthly = []

    vistorYearNumber =[]
    visitorNumberYearly = []

    monthly_visitor = VisitorCount.objects.all().values(
    'date_of_record__month'
    ).annotate(
        total_in_month=Count('ip') # take visitor_id or whatever you want to count
        ).order_by('date_of_record__month')
    
    yearly_visitor = VisitorCount.objects.all().values('date_of_record__year').annotate(
        total_in_year= Count('ip')
        ).order_by('date_of_record__year')

    for i in range(len(monthly_visitor)):

        visitorMonthNumber.append(monthly_visitor[i]['date_of_record__month'])
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
    

def user_data(request):  #for users

    userspermonth = []
    usersmonthnumber =[]

    usersperyear =[]
    usersyearnumber = []
    
    monthly_users = CustomUser.objects.all().values(
    'date_joined__month'
    ).exclude(is_staff = True).exclude(is_active=False).annotate(
        total_in_month=Count('email') # take visitor_id or whatever you want to count
        ).order_by('date_joined__month')

    yearly_users = CustomUser.objects.all().values('date_joined__year').exclude(is_staff = True).exclude(is_active =False).annotate(
        total_in_year= Count('email')
        ).order_by('date_joined__year')

    for i in range(len(monthly_users)):

        usersmonthnumber.append(monthly_users[i]['date_joined__month'])
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
    