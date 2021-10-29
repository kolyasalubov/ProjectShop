# Generated by Django 3.2.6 on 2021-10-29 10:22

import UserApp.managers
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ProductApp', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('telegram_id', models.CharField(default=None, max_length=40, null=True, unique=True, verbose_name='telegram id')),
                ('first_name', models.CharField(max_length=40, verbose_name='first name')),
                ('last_name', models.CharField(max_length=40, verbose_name='last name')),
                ('middle_name', models.CharField(blank=True, max_length=40, verbose_name='middle name')),
                ('profile_pic', models.ImageField(default='default_profile_pictures/default_pic.svg', upload_to='profile_pictures/', verbose_name='profile picture')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('register_date', models.DateField(auto_now_add=True, verbose_name='date of registration')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='phone number')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('role', models.IntegerField(choices=[(0, 'user'), (1, 'admin')], default=0, verbose_name='role')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_bot', models.BooleanField(default=False, verbose_name='is bot')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('wishlist', models.ManyToManyField(blank=True, related_name='wishlist', to='ProductApp.Product')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', UserApp.managers.UserManager()),
            ],
        ),
    ]
