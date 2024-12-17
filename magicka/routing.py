# magicka/routing.py

from django.urls import re_path
from .consumers import AttackNotificationConsumer

websocket_urlpatterns = [
    re_path(r'ws/battle/(?P<room_name>\w+)/$', AttackNotificationConsumer.as_asgi()),
]
