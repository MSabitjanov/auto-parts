# Generated by Django 4.2.5 on 2023-10-24 11:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communication', '0009_alter_chat_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='seller_name',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Последнее сообщение'),
        ),
        migrations.AddField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(related_name='chats', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
    ]
