# Generated by Django 3.2.6 on 2021-11-01 14:14

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postal_code', models.CharField(max_length=20, verbose_name='postal code')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('region', models.CharField(max_length=50, verbose_name='region')),
                ('city', models.CharField(max_length=50, verbose_name='city')),
                ('post_office', models.IntegerField(verbose_name='post office')),
            ],
            options={
                'verbose_name': 'Shipping address',
                'verbose_name_plural': 'Shipping addresses',
            },
        ),
    ]
