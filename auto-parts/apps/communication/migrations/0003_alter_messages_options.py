# Generated by Django 4.2.5 on 2023-10-08 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
    ]