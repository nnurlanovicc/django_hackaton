from rest_framework.serializers import ModelSerializer,  ReadOnlyField
from .models import Comment


class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        comment = Comment.objects.create(author=user, **validated_data)
        return comment        
