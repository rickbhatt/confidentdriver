from django.shortcuts import render, redirect

from datetime import datetime, date


from home.models import *

from account.models import *

from .tasks import *

from .decorators import OnlySuperuser
# Create your views here.




@OnlySuperuser
def dashboard(request):

    all_users = CustomUser.objects.all().exclude(is_staff = True).count()
    
    all_users_bydate = CustomUser.objects.all().filter(date_joined__contains= datetime.today().date()).count()

    all_contracts = Contract.objects.all().count()

    contract_signed_today = Contract.objects.all().filter(date_of_acceptance__contains= datetime.today().date()).count()

    contract_expire_today  = Contract.objects.all().filter(date_of_expiration__contains= datetime.today().date()).count()
    

    # print('allcontracts', all_contracts)
    
    context = {'all_users': all_users, 'all_users_bydate':all_users_bydate,'all_contracts':all_contracts ,'contract_signed_today':contract_signed_today,'contract_expire_today': contract_expire_today}

    return render(request, 'control_pannel.html', context)