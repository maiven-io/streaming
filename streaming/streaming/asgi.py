# asgi.py

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from openstream.routing import websocket_urlpatterns  # Import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'streaming.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Add WebSocket URL routing
        )
    ),
})
