# Generated by Django 5.0 on 2024-01-07 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0030_alter_post_text_after'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text_before',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Текст вначале (необъязательно)'),
        ),
    ]
