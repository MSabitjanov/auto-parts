# Generated by Django 4.2.5 on 2024-01-02 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_master_description_en_master_description_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='company_info_en',
            field=models.TextField(blank=True, null=True, verbose_name='Информация о компании'),
        ),
        migrations.AddField(
            model_name='seller',
            name='company_info_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Информация о компании'),
        ),
        migrations.AddField(
            model_name='seller',
            name='company_info_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Информация о компании'),
        ),
    ]