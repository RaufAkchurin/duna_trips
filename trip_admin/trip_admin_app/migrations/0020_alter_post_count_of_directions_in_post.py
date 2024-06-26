# Generated by Django 4.2.7 on 2023-12-25 10:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0019_remove_destination_count_of_destinations_in_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='count_of_directions_in_post',
            field=models.IntegerField(default=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Направлений полета в посте'),
        ),
    ]
