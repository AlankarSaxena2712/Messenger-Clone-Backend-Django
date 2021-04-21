from django.contrib import admin

from .models import *


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'room', 'sender']
    list_display_links = ['id', 'content']
