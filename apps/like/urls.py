from django.urls import path
from .views import LikeCreateAndListView

app_name = 'your_app_name'

urlpatterns = [
    path('likes/', LikeCreateAndListView.as_view(), name='like-list-create'),
]

