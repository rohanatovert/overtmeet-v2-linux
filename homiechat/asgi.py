"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homiechat.settings.development')
django.setup()
from rooms.consumers import NotificationConsumer, OnlineStatusConsumer, PersonalChatConsumer, CallConsumer, TestConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
# from decouple import config



application = get_asgi_application()

application = ProtocolTypeRouter({
    # Just HTTP for now. (We can add other protocols later.)
  # add authmiddlewarestack later
  "http": get_asgi_application(),
  "websocket": URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
            path('ws/notify/', NotificationConsumer.as_asgi()),
            path('ws/online/', OnlineStatusConsumer.as_asgi()),
            path('ws/<int:id>/call/', CallConsumer.as_asgi()),
        ])
    ,
}) 

# application = ProtocolTypeRouter({
#     'websocket' : URLRouter([
#         path('ws/test/', TestConsumer)
#     ])
# })

