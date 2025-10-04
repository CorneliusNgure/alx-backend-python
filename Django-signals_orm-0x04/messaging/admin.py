from django.contrib import admin
from .models import Message, Notification, MessageHistory
from django.urls import path, include

ulrpatterns = [
    path("admin/", admin.site.urls)
]

admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(MessageHistory)