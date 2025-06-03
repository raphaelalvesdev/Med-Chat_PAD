# chat/urls.py

from django.urls import path
from . import views

app_name = 'chat' # Namespace para as URLs do app

urlpatterns = [
    path('', views.chat_page, name='chat_page'), # URL para a página de chat
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'), # URL para a API do chatbot
]