# Generated by Django 4.0 on 2022-04-10 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0012_remove_video_caption'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='room_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Base.room'),
        ),
    ]