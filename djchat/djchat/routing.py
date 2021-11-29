import chat.routing
from channels.auth import AuthMiddlewareStack  # type: ignore
from channels.routing import ProtocolTypeRouter, URLRouter  # type: ignore

application = ProtocolTypeRouter({"websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))})
