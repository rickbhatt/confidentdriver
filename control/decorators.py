from django.http import HttpResponse
from django.shortcuts import redirect

def OnlySuperuser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('you are not authorised')
    return wrapper_func