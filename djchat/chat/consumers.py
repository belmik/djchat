import json
from datetime import datetime

from channels.db import database_sync_to_async  # type: ignore
from channels.generic.websocket import AsyncWebsocketConsumer  # type: ignore
from chat.models import ChatMessage
from django.core.exceptions import ValidationError


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
        self.post_datetime = self.get_post_datetime()

        await self.save_message()
        if self.cur_datetime == self.post_datetime:
            await self.channel_layer.group_send(self.group_name, {"type": "chat_message", "message": message})

    async def chat_message(self, event: dict[str, str]) -> None:
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_message(self) -> bool:
        try:
            ChatMessage.objects.create(user=self.user, message=self.data["message"], post_time=self.post_datetime)
        except ValidationError:
            return False

        return True

    def format_msg(self) -> str:

        message = f"<p><b>{self.user.username}</b><br>"
        message += f'<b>{self.cur_datetime.strftime("%d.%m.%y %H:%M")} > </b>'
        message += f'{self.data["message"]}</p>'

        return message

    def get_post_datetime(self) -> datetime:

        if "pub_datetime" in self.data:
            try:
                post_time = datetime.fromisoformat(self.data["pub_datetime"])
            except ValueError:
                return self.cur_datetime

            return post_time

        return self.cur_datetime
