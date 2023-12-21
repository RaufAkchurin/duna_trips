# Generated by Django 4.2.7 on 2023-12-21 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0008_remove_destination_country_destination_chanel'),
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