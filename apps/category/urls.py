from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailUpdateDeleteView,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<str:pk>/', CategoryDetailUpdateDeleteView.as_view(), name='category-detail'),
]
