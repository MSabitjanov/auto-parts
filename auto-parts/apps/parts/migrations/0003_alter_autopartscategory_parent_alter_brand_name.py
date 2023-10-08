# Generated by Django 4.2.5 on 2023-10-08 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autopartscategory',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Если это родительская категория, то оставьте это поле пустым.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='parts.autopartscategory', verbose_name='Родительская категория'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название бренда'),
        ),
    ]
