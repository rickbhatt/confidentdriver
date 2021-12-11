from django.urls import path

from . import views


urlpatterns=[
    path('control-pannel',views.dashboard, name='control-pannel'),

]