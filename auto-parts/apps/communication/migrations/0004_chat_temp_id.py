# Generated by Django 4.2.5 on 2023-10-24 05:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0003_alter_messages_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='temp_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]