from django.urls import path
from .views import InteractionListCreateView, ChatInteractionView

urlpatterns = [
    path('', InteractionListCreateView.as_view(), name='interaction-list'),
    path('chat/', ChatInteractionView.as_view(), name='chat-interaction'),
]