from django.contrib import admin
from django.urls import path
from.views import join,chat,signuppage,loginpage

urlpatterns = [
    path('join/',join,name="join"),
    path('chat/<room_code>/',chat,name="chat"),
    path('login/',loginpage,name="loginpage"),
    path('signup/',signuppage,name="signuppage")
]
