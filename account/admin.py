from django.contrib import admin

from .models import CustomUser
# Register your models here.

# admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=('email', 'full_name', 'phone_no','plan', 'date_joined', 'is_active')
    ordering= ('full_name',)
    search_fields=('email', 'phone_no', 'date_joined')