from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.account.permissions import IsAuthorPermission
from rest_framework.generics import GenericAPIView
from .serializers import CommentSerializer
from .models import Comment
from rest_framework import status
from rest_framework.response import Response

class CommentView(GenericAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny] 

    permission_classes_by_action = {
        'create': [IsAuthenticated],
        'update': [IsAuthorPermission],
        'partial_update': [IsAuthorPermission],
        'destroy': [IsAuthorPermission],
        'list': [AllowAny],
        'retrieve': [AllowAny],
    }

    def get_permissions(self):

        if self.request.method == 'POST':
            self.action = 'create'
        elif self.request.method in ['PUT', 'PATCH']:
            self.action = 'update'
        elif self.request.method == 'DELETE':
            self.action = 'destroy'
        else:
            self.action = 'list'
        
        permissions = self.permission_classes_by_action.get(self.action, self.permission_classes)
        return [permission() for permission in permissions]
    

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance, data=request.data, partial=False)
        if serializer.is_valid():
            if instance.author == request.user: 
                serializer.save()
                return Response(serializer.data)
            return Response({"ошибка": "Вы не автор этого комментария."}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            if instance.author == request.user:  
                serializer.save()
                return Response(serializer.data)
            return Response({"ошибка": "Вы не автор этого комментария."}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:  
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"ошибка": "Вы не автор этого комментария."}, status=status.HTTP_403_FORBIDDEN)