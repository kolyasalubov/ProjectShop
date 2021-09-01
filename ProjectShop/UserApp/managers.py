from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number: str, first_name: str, last_name: str, email: str, \
                    password: str):
        """
            Creates and saves a User with the phone number, first name, last name, email, password
            return: user instance
        """
        if not phone_number:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone_number=phone_number,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number: str, first_name: str, last_name: str, email: str, password: str):
        """
            Creates and saves a SuperUser with the phone number, first name, last name, email, password
            return: user instance
        """
        user = self.create_user(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
        )
        user.role = 1
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
