# Generated by Django 4.2.7 on 2023-12-22 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0014_remove_destination_chanel_remove_post_tickets_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_viewed_destination_id',
            field=models.PositiveIntegerField(default=1),
        ),
    ]