from django.urls import path
from .views import CommentView

urlpatterns = [
    path('comments/', CommentView.as_view()),
    path('comments/<int:pk>/', CommentView.as_view()),
]

