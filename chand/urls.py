from django.contrib import admin
from django.urls import path
from.views import home,chat

urlpatterns = [
    path('',home,name="home"),
    path('chat/<room_code>/',chat,name="chat")
]
