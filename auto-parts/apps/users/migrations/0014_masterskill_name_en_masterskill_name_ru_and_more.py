# Generated by Django 4.2.5 on 2024-01-02 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_seller_company_info_en_seller_company_info_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterskill',
            name='name_en',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='masterskill',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='masterskill',
            name='name_uz',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='region',
            name='name_en',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='region',
            name='name_ru',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Название'),
        ),
        migrations.AddField(
            model_name='region',
            name='name_uz',
            field=models.CharField(max_length=50, null=True, unique=True, verbose_name='Название'),
        ),
    ]
