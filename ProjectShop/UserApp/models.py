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

        first_name: Describes user`s first name
        type: str, max_length: 40, required field

        last_name: Describes user`s last name
        type: str, max_length: 40, required field

        middle_name: Describes user`s middle name
        type: str, max_length: 40

        birth_date: Describes user`s birth date
        type: datetime.date

        register_date: Describes the date of user`s registration, auto-filled with the date user has been created
        type: datetime.date, CAN`T BE CHANGED

        phone_number: Describes user`s phone number in international format(like +380 00 000 00 00)
        type: PhoneNumber, used as a username field, required field, unique field
        more about phoneNumber: https://github.com/stefanfoulis/django-phonenumber-field

        email: Describes user`s email
        type: str, required field, unique field

        role: Describes user`s role, admin(1) is an administrator
        type: int, default value = 0, required field
    """
    first_name = models.CharField(verbose_name='first name', blank=False, null=False, max_length=40)
    last_name = models.CharField(verbose_name='last name', blank=False, null=False, max_length=40)
    middle_name = models.CharField(verbose_name='middle name', blank=True, null=False, max_length=40)

    birth_date = models.DateField(verbose_name='date of birth', blank=True, null=True, auto_now=False, auto_now_add=False)
    register_date = models.DateField(verbose_name='date of registration', blank=False, null=False,
                                     auto_now=False, auto_now_add=True, editable=False)

    phone_number = PhoneNumberField(verbose_name='phone number', blank=False, null=False, unique=True)
    email = models.EmailField(verbose_name='email', blank=False, null=False, unique=True)
    role = models.IntegerField(verbose_name='role', default=0, choices=ROLE_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self) -> int:
        return self.role
