# Generated by Django 4.2.5 on 2024-02-18 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_alter_autopartsreview_comment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_review_numbers', models.PositiveIntegerField(default=0)),
                ('total_review_score', models.PositiveIntegerField(default=0)),
                ('auto_parts_review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='review.autopartsreview')),
                ('master_review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='review.masterreview')),
            ],
        ),
    ]
