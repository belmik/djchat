from django.db import models
from django.contrib.auth.models import User


class ChatMessage(models.Model):
    user = models.ForeignKey(User, verbose_name="пользователь", on_delete=models.PROTECT)
    message = models.TextField(verbose_name="Сообщение")
    post_time = models.DateTimeField(verbose_name="Время публикации", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self) -> str:
        return f"{self.user.username} <{self.post_time}>: {self.message}"
