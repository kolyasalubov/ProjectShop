# Generated by Django 3.2 on 2021-08-31 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='birthDate',
            new_name='birth_date',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='firstName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lastName',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='middleName',
            new_name='middle_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phoneNumber',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='registerDate',
            new_name='register_date',
        ),
    ]