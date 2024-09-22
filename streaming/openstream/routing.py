from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .OpenAIConsumer import OpenAIConsumer

websocket_urlpatterns = [
    path('ws/openstream/<str:thread_id>/', OpenAIConsumer.as_asgi()),
]
