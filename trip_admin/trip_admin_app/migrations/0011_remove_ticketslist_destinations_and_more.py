# Generated by Django 4.2.7 on 2023-12-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0010_remove_ticketslist_destinations_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketslist',
            name='destinations',
        ),
        migrations.AddField(
            model_name='ticketslist',
            name='destinations',
            field=models.ManyToManyField(to='trip_admin_app.destination', verbose_name='Направления'),
        ),
    ]
