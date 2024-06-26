# Generated by Django 4.2.7 on 2023-12-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0016_alter_post_last_viewed_destination_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='last_viewed_destination_id',
        ),
        migrations.AddField(
            model_name='post',
            name='last_viewed_destination_index',
            field=models.IntegerField(default=-1, verbose_name='Индекс последнего опубликованого направления'),
        ),
    ]
