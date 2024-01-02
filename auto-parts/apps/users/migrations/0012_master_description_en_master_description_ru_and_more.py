# Generated by Django 4.2.5 on 2024-01-01 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_master_address_master_company_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='master',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='master',
            name='description_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]