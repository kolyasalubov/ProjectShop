from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phoneNumber: str, firstName: str, lastName: str, email: str, \
                    password: str):
        """
            Creates and saves a User with the phone number, first name, last name, email, password
            return: user instance
        """
        if not phoneNumber:
            raise ValueError('Users must have an phone number')

        email = self.normalize_email(email)

        user = self.model(
            phoneNumber=phoneNumber,
            email=email,
            firstName=firstName,
            lastName=lastName,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phoneNumber: str, firstName: str, lastName: str, email: str, password: str):
        """
            Creates and saves a SuperUser with the phone number, first name, last name, email, password
            return: user instance
        """
        user = self.create_user(
            phoneNumber=phoneNumber,
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password,
        )
        user.role = 1
        user.is_superuser = True
        user.save(using=self._db)

        return user
