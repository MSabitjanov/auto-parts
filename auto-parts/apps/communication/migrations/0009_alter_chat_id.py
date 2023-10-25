# Generated by Django 4.2.5 on 2023-10-24 10:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0008_alter_chat_last_message_received_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]