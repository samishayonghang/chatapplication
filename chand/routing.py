from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chand/<room_code>/', consumers.ChatConsumer.as_asgi()),
]
