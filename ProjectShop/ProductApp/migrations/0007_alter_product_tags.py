# Generated by Django 3.2.6 on 2021-09-21 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0006_auto_20210921_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(related_query_name='products', to='ProductApp.Tag'),
        ),
    ]
