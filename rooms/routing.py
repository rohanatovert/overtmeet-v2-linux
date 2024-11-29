# from django.urls import re_path
# from channels.routing import ProtocolTypeRouter, URLRouter
# from . import consumers

# # websocket_urlpatterns = [
# #     path('join_chat_view/<str:room_code>/', consumers.ChatConsumer.as_asgi()),
# # ]

# websocket_urlpatterns = [
#         re_path("wss/calling/", consumers.MyWebSocketConsumer.as_asgi()),
#     ]