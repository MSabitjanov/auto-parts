# Generated by Django 4.2.5 on 2023-10-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_seller_company_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активный'),
        ),
    ]
