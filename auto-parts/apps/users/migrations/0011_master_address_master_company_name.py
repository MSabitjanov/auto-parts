# Generated by Django 4.2.5 on 2023-12-17 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_seller_seller_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='master',
            name='company_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название Компании'),
        ),
    ]
