# Generated by Django 4.2.5 on 2023-10-22 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0003_alter_autopartscategory_parent_alter_brand_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0008_alter_region_options_alter_master_skilled_at'),
        ('review', '0004_review_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoPartsReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('reviewed_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auto_parts_reviews', to='parts.autoparts', verbose_name='Запчасть')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв запчасти',
                'verbose_name_plural': 'Отзывы запчастей',
            },
        ),
        migrations.CreateModel(
            name='MasterReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('rating', models.PositiveSmallIntegerField(verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('reviewed_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master_reviews', to='users.master', verbose_name='Мастер')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_reviews', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв мастера',
                'verbose_name_plural': 'Отзывы мастеров',
            },
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
