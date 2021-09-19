from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image, UnidentifiedImageError

from UserApp.managers import UserManager


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

        profile_pic: User`s avatar
        type: ImageField, default path = media/default_profile_pictures/default_pic.svg

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
    first_name = models.CharField(verbose_name=_('first name'), blank=False, null=False, max_length=40)
    last_name = models.CharField(verbose_name=_('last name'), blank=False, null=False, max_length=40)
    middle_name = models.CharField(verbose_name=_('middle name'), blank=True, null=False, max_length=40)

    profile_pic = models.ImageField(verbose_name=_('profile picture'), upload_to='profile_pictures/',
                                    default='default_profile_pictures/default_pic.svg')
    birth_date = models.DateField(verbose_name=_('date of birth'), blank=True, null=True, auto_now=False,
                                  auto_now_add=False)
    register_date = models.DateField(verbose_name=_('date of registration'), blank=False, null=False,
                                     auto_now=False, auto_now_add=True, editable=False)

    phone_number = PhoneNumberField(verbose_name=_('phone number'), blank=False, null=False, unique=True)
    email = models.EmailField(verbose_name=_('email'), blank=False, null=False, unique=True)
    role = models.IntegerField(verbose_name=_('role'), default=0, choices=ROLE_CHOICES)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self) -> str:
        return self.email

    def get_info(self):
        return self.profile_pic.path

    def has_perm(self, perm, obj=None):
        return self.role

    def has_module_perms(self, app_label):
        return self.role

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        try:
            # Need this try block because default image is .svg format
            # Can be replaced with checking if self.profile_pic.name is not default
            image_path = self.profile_pic.path

            img = Image.open(image_path)

            if img.height > 300 or img.width > 300:
                new_img_size = (300, 300)
                img.thumbnail(new_img_size)
                img.save(image_path)
        except UnidentifiedImageError:
            pass

    @property
    def is_staff(self) -> int:
        return self.role
