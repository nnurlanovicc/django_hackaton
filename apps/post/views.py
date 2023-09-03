from rest_framework import generics, viewsets, filters
from .models import Post
from apps.like.models import LikePost,LikeComment
from apps.comment.models import Comment
from .serializers import PostDetailSerializer, PostListSerializer
import django_filters
from rest_framework.permissions import AllowAny
from apps.account.permissions import IsAuthorPermission
from rest_framework.decorators import action
from rest_framework.response import Response

class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
        ]
    filterset_fields = ['tags__slug', 'category', 'author']
    search_fields = ['title', 'body'] 
    ordering_fields = ['created_at', 'title']   

    @action(['POST'], detail=True)
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = LikePost.objects.get(post=post, author=user)
            like.delete()
            message = 'disliked'
            status = 204
        except LikePost.DoesNotExist:
            LikePost.objects.create(post=post, author=user)
            message = 'liked'
            status = 201
        return Response(message, status=status)
    
    def like_comment(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = LikeComment.objects.get(post=post, author=user)
            like.delete()
            message = 'disliked'
            status = 204
        except LikeComment.DoesNotExist:
            LikeComment.objects.create(post=post, author=user)
            message = 'liked'
            status = 201
        return Response(message, status=status)


    @action(['POST'], detail=True)
    def comment(self, request, pk=None):
        post = self.get_object()
        user = request.user
        comment = Comment.objects.create(post=post, author=user)
        return Response(comment, status=201)



    def get_serializer_class(self):
    
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer
    
    def get_permissions(self):

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
