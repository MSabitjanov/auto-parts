# Generated by Django 4.2.5 on 2024-01-03 16:17

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_masterskill_name_en_masterskill_name_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Местоположение'),
        ),
    ]
