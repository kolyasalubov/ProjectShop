# Generated by Django 3.2.6 on 2021-09-16 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card')], default='Cash', max_length=4),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=7),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_status',
            field=models.CharField(choices=[('Planning', 'Planning'), ('Shipping', 'Shipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Planning', max_length=9),
        ),
    ]
