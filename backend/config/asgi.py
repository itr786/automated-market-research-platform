import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from research.consumers import ResearchProgressConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([re_path(r"ws/research/(?P<brief_id>\\d+)/$", ResearchProgressConsumer.as_asgi())]),
})
