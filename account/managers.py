from django.contrib.auth.base_user import BaseUserManager

from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    # CUSTOM USER MODEL FOR USER WHERE EMAIL IS THE USERNAME FOR AUTHENTICATION RATHER THEN USERNAME

    
    
    def create_superuser(self, email, full_name, password, **other_fields):

    # CREATE AND SAVE SUPERUSER WITH THE GIVEN EMAIL AND PASSWORD

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('is staff must be set to true'))
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('is superuser must be set to true'))
        
        return self.create_user(email, full_name, password, **other_fields)

    
    def create_user(self, email,full_name, password, **other_fields):

    # CREATE AND SAVE USER WITH THE GIVEN EMAIL AND PASSWORD

        if not email:
            raise ValueError(_('The Email must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,**other_fields)
        user.set_password(password)
        user.save()
        return user


            



