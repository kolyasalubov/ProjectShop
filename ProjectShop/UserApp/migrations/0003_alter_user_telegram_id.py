# Generated by Django 3.2.6 on 2021-09-23 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0002_user_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.IntegerField(null=True, unique=True, verbose_name='telegram id'),
        ),
    ]
