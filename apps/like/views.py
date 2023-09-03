from rest_framework.views import APIView
from .models import LikePost, LikeComment
from .serializers import LikePostSerializer, LikeCommentSerializer
from rest_framework.response import Response
from rest_framework import status

class LikePostView(APIView):
    def get(self, request, *args, **kwargs):
        likes = LikePost.objects.all()
        serializer = LikePostSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LikePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeCommentView(APIView):
    def get(self, request, *args, **kwargs):
        likes = LikeComment.objects.all()
        serializer = LikeCommentSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LikeCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
