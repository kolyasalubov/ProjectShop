# Generated by Django 3.2.6 on 2021-09-20 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductApp', '0004_alter_productmedia_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmedia',
            name='image',
            field=models.ImageField(default='default_image/default_image.png', upload_to='product_media_image'),
        ),
    ]