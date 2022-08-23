from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Topic)
admin.site.register(Room)
admin.site.register(Video)
admin.site.register(Message)
