from rest_framework.permissions import AllowAny, IsAuthenticated
from account.permissions import IsAuthorPermission
from rest_framework.generics import GenericAPIView
from .serializers import CommentSerializer
from .models import Comment

class CommentView(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
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
        return [permission() for permission in self.permission_classes_by_action.get(self.action, self.permission_classes)]
