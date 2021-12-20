from django.shortcuts import render, redirect

from datetime import datetime, date

from . models import VisitorCount

from home.models import *

from account.models import *

from .tasks import *

from .decorators import OnlySuperuser

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_control


# Create your views here.



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@OnlySuperuser
@login_required(login_url='login')
def dashboard(request):

    all_users = CustomUser.objects.all().filter(is_active = True).exclude(is_staff = True).count()
    
    all_users_bydate = CustomUser.objects.all().filter(date_joined__contains= datetime.today().date()).exclude(is_staff = True).count()

    all_contracts = Contract.objects.all().count()

    contract_signed_today = Contract.objects.all().filter(date_of_acceptance__contains= datetime.today().date()).count()

    contract_expire_today  = Contract.objects.all().filter(date_of_expiration__contains= datetime.today().date()).count()
    
    visitor_today = VisitorCount.objects.all().filter(date_of_record__icontains = datetime.today().date()).count()

    # print('allcontracts', all_contracts)
    
    context = {'all_users': all_users, 'all_users_bydate':all_users_bydate,'all_contracts':all_contracts ,'contract_signed_today':contract_signed_today,'contract_expire_today': contract_expire_today, 'visitor_today': visitor_today}

    return render(request, 'dashboard.html', context)