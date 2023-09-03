from django.urls import path
from .views import LikePostView,LikeCommentView


urlpatterns = [
    path('like_post/', LikePostView.as_view()),
    path('like_comment/', LikeCommentView.as_view())
]

