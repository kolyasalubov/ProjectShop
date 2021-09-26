# Generated by Django 3.2.6 on 2021-09-26 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shipping', '0001_initial'),
        ('ProductApp', '0003_auto_20210925_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card')], default='Cash', max_length=4)),
                ('shipping_status', models.CharField(choices=[('Planning', 'Planning'), ('Shipping', 'Shipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Planning', max_length=9)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=7)),
                ('shippingAddress_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shipping.shippingmodel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_items_qantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.ordermodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProductApp.product')),
            ],
        ),
    ]
