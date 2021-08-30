from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager

ROLE_CHOICES = (
    (0, 'user'),
    (1, 'admin'),
)


class User(AbstractBaseUser, PermissionsMixin):
    """
        This class represents basic user.
        =======================================
        Attributes:

        firstName: Describes user`s first name
        type: str, max_length: 40, required field

        lastName: Describes user`s last name
        type: str, max_length: 40, required field

        middleName: Describes user`s middle name
        type: str, max_length: 40

        birthDate: Describes user`s birth date
        type: datetime.date

        registerDate: Describes the date of user`s registration, auto-filled with the date user has been created
        type: datetime.date, CAN`T BE CHANGED

        phoneNumber: Describes user`s phone number in international format(like +380 00 000 00 00)
        type: PhoneNumber, used as a username field, required field, unique field
        more about phoneNumber: https://github.com/stefanfoulis/django-phonenumber-field

        email: Describes user`s email
        type: str, required field, unique field

        role: Describes user`s role, admin(1) is an administrator
        type: int, default value = 0, required field
    """
    firstName = models.CharField(verbose_name='first name', blank=False, null=False, max_length=40)
    lastName = models.CharField(verbose_name='last name', blank=False, null=False, max_length=40)
    middleName = models.CharField(verbose_name='middle name', blank=True, null=False, max_length=40)

    birthDate = models.DateField(verbose_name='date of birth', blank=True, null=True, auto_now=False, auto_now_add=False)
    registerDate = models.DateField(verbose_name='date of registration', blank=False, null=False, \
                                    auto_now=False, auto_now_add=True, editable=False)

    phoneNumber = PhoneNumberField(verbose_name='phone number', blank=False, null=False, unique=True)
    email = models.EmailField(verbose_name='email', blank=False, null=False, unique=True)
    role = models.IntegerField(verbose_name='role', default=0, choices=ROLE_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'email']

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self) -> int:
        return self.role
