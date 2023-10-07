# Generated by Django 4.2.5 on 2023-10-03 01:41

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='AutoPartsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('characteristics', taggit.managers.TaggableManager(help_text='Введите характеристики через запятую(Например, если это шина, то радиус, ширина, высота. Если это двигатель, то объем, мощность, тип. )', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Характеристики')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='parts.autopartscategory')),
            ],
            options={
                'verbose_name': 'Категория автозапчастей',
                'verbose_name_plural': 'Категории автозапчастей',
            },
        ),
        migrations.CreateModel(
            name='AutoParts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_new', models.BooleanField(default=True, verbose_name='Новый')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('characteristics', models.JSONField(blank=True, null=True, verbose_name='Дополнительные атрибуты')),
                ('date_of_pubication', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')),
                ('rating', models.FloatField(default=0.0, verbose_name='Рейтинг')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='parts.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='parts', to='parts.autopartscategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Автозапчасть',
                'verbose_name_plural': 'Автозапчасти',
            },
        ),
    ]
