
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import security.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shaas_smarthomy.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            security.routing.websocket_urlpatterns
        )
    ),
})