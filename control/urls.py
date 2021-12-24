from django.urls import path

from . import views


urlpatterns=[
    path('dashboard',views.dashboard, name='dashboard'),
    path('analytics',views.analytics, name='analytics'),
    path('visitor-data',views.visitor_data, name='visitor-data'),
    path('user-data',views.user_data, name='user-data'),




]