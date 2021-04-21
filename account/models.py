from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Room(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.CharField(max_length=300, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content
