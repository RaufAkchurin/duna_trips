# Generated by Django 4.2.7 on 2023-12-21 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0009_remove_ticketslist_destinations_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketslist',
            name='destinations',
        ),
        migrations.AddField(
            model_name='ticketslist',
            name='destinations',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trip_admin_app.destination', verbose_name='Направления'),
            preserve_default=False,
        ),
    ]