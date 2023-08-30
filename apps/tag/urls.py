from django.urls import path
from .views import (
    TagListCreateView,
    TagDetailUpdateDeleteView,
)

urlpatterns = [
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<str:pk>/', TagDetailUpdateDeleteView.as_view(), name='tag-detail'),
]
