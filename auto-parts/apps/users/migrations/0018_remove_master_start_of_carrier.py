# Generated by Django 4.2.5 on 2024-02-24 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_user_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master',
            name='start_of_carrier',
        ),
    ]
