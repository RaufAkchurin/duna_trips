# Generated by Django 5.0 on 2024-01-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0022_alter_post_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
