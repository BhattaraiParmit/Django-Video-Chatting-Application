# Generated by Django 4.0 on 2022-04-08 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0007_room_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='media/')),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='video',
        ),
    ]