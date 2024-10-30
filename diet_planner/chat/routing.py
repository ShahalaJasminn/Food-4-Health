from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/consultation/<int:consultation_id>/', consumers.ChatConsumer.as_asgi()),
]
