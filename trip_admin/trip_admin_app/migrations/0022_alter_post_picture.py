# Generated by Django 4.2.7 on 2023-12-25 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_admin_app', '0021_post_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(upload_to='post_pictures/', verbose_name='Изображение поста'),
        ),
    ]
