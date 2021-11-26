import asyncio
import json
from datetime import datetime
from typing import Optional

from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore
from channels.db import database_sync_to_async  # type: ignore
from django.core.exceptions import ValidationError
from chat.models import ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.group_name = "public_chat"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data: str) -> None:
        self.cur_datetime = datetime.now()
        self.user = self.scope["user"]
        self.data = json.loads(text_data)
        message = self.format_msg()

        delay = None
        if "delay" in self.data:
            delay = int(self.data["delay"])

        await self.process_msg(message, sleep=delay)

    async def chat_message(self, event: dict[str, str]) -> None:
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def process_msg(self, message: str, sleep: Optional[int] = None) -> None:
        if sleep:
            await asyncio.sleep(sleep)

        await self.save_message()
        await self.channel_layer.group_send(self.group_name, {"type": "chat_message", "message": message})

    @database_sync_to_async
    def save_message(self) -> bool:
        try:
            ChatMessage.objects.create(user=self.user, message=self.data["message"], post_time=self.cur_datetime)
        except ValidationError:
            return False

        return True

    def format_msg(self) -> str:

        message = f"<p><b>{self.user.username}</b><br>"
        message += f'<b>{self.cur_datetime.strftime("%d.%m.%y %H:%M")} > </b>'
        message += f'{self.data["message"]}</p>'

        return message
