from django.urls import re_path 
from . import consumers

websocket_urlpatterns = [
    re_path(r"manga/ws/(?P<session_id>[\w-]+)$", consumers.WebsocketConsumer.as_asgi())
]