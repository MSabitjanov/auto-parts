# Generated by Django 4.2.5 on 2023-10-24 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0010_remove_chat_customer_name_remove_chat_seller_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активный чат'),
        ),
    ]
