# Generated by Django 3.2.6 on 2021-09-17 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_media_image'),
        ),
        migrations.AlterField(
            model_name='productmedia',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='media', to='ProductApp.product'),
        ),
    ]
