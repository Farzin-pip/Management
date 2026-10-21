from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password, role='resident'):
        if not phone_number:
            raise ValueError('Phone Number is required')

        if not first_name:
            raise ValueError('First Name is required')

        if not last_name:
            raise ValueError('Last Name is required')

        user = self.model(phone_number=phone_number, first_name=first_name, last_name=last_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number, first_name, last_name, password):
        user = self.create_user(phone_number, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.role = 'admin'
        user.save(using=self._db)
        return user
