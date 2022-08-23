"""
ASGI config for Project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from django.urls import path
from django.core.asgi import get_asgi_application
from Base.consumers import *
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')

application = get_asgi_application()


ws_pattern = [
    path('ws/<room_code>/<created>/', ConferenceRoom.as_asgi())
]


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_pattern)
    )
})