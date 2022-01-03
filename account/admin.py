from django.contrib import admin

from .models import CustomUser, ForgetPassword
# Register your models here.

# admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=('email', 'full_name', 'phone_no', 'type_of_plan','plan', 'date_joined', 'is_active')
    ordering= ('full_name',)
    search_fields=('email', 'phone_no', 'date_joined')

@admin.register(ForgetPassword)
class ForgetPasswordAdmin(admin.ModelAdmin):
    list_display=('user', 'forget_password_token', 'created_at')
