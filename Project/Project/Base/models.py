from email.policy import default
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

import string
import random


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True, unique=True)
    # bio = 
    avatar = models.ImageField(null=True, blank=True, default='default.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Topic(models.Model):
    name = models.CharField(max_length=100, null= True)

    def __str__(self):
        return self.name


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



class Room(models.Model):
    room_code = models.CharField(max_length=100, blank=True)
    host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True)
    description =  models.TextField(null=True, blank=True)
    participant = models.ManyToManyField(CustomUser, related_name = 'participant', blank=True)
    isLive = models.BooleanField(default=False)
    created_data = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

   

    def save(self, *args, **kwargs):
        if not len(self.room_code):
            self.room_code = random_string_generator()

        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return self.name    




class Video(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    video = models.FileField(upload_to='media/', null= True, blank=True)


    def __str__(self):
        return str(self.id)


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.body


@receiver(post_save, sender = Message)
def send_message(sender, instance, created,  **kwargs):
    if created:
        print("hello message")
        channel_layer = get_channel_layer()
        data = {}
        # message = instance.objects.filter() 
        data['image'] = instance.user.avatar.url
        data['user'] = instance.user.username
        data['message'] = instance.body

        async_to_sync(channel_layer.group_send)(
            "room_%s" % instance.room.room_code, {
                'type': 'order_message',
                'message': data
            }
        )
    







# class Room(models.Model):
#     room_code = models.CharField(max_length=100, blank=True)
#     host = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=100, null=True)
#     description =  models.TextField(null=True, blank=True)
#     participant = models.ManyToManyField(CustomUser, related_name = 'participant', blank=True)
#     created_data = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)

   

#     def save(self, *args, **kwargs):
#         if not len(self.room_code):
#             self.room_code = random_string_generator()

#         super(Room, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.name    


# class Video(models.Model):
#     # caption = models.CharField(max_length=100, null=True)
#     video = models.FileField(upload_to='media/', null= True, blank=True)


#     def __str__(self):
#         return str(self.id)
    