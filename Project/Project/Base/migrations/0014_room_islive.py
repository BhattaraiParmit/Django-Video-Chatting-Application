# Generated by Django 4.0 on 2022-04-10 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0013_video_room_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='isLive',
            field=models.BooleanField(default=False),
        ),
    ]
