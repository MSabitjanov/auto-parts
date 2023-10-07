# Generated by Django 4.2.5 on 2023-10-07 12:28

import apps.images.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parts', '0002_initial'),
        ('users', '0004_alter_masterskill_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.images.models.get_upload_path_for_master, verbose_name='Изображение')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='users.master', verbose_name='Мастер')),
            ],
            options={
                'verbose_name': 'Изображение мастера',
                'verbose_name_plural': 'Изображения мастеров',
            },
        ),
        migrations.CreateModel(
            name='AutoPartsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.images.models.get_upload_path_for_part, verbose_name='Изображение')),
                ('auto_part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='parts.autoparts', verbose_name='Автозапчасть')),
            ],
            options={
                'verbose_name': 'Изображение автозапчасти',
                'verbose_name_plural': 'Изображения автозапчастей',
            },
        ),
    ]
