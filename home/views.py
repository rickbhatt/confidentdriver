from django.shortcuts import render

# Create your views here.


def home(request):

    return render(request, 'index.html')


def price(request):

    return render(request, 'price.html')