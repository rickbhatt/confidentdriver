from django.contrib import admin

from .models import CustomUser, ForgetPassword

from django.contrib.auth.admin import UserAdmin 

# Register your models here.

# admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display=('email', 'full_name', 'phone_no', 'type_of_plan','plan', 'date_joined', 'is_active')
    ordering= ('full_name',)
    search_fields=('email', 'phone_no', 'date_joined')

    fieldsets = (
        (None, {'fields':('email','full_name','phone_no','age','address','type_of_plan','plan','date_joined','password',),}),
        ('Permissions',{'fields': ('is_staff', 'is_active', 'groups', 'user_permissions',)}),
        )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name','phone_no','age','address','type_of_plan','plan','date_joined','password1','password2',)}
         ),
    )


@admin.register(ForgetPassword)
class ForgetPasswordAdmin(admin.ModelAdmin):
    list_display=('user', 'forget_password_token', 'created_at')
