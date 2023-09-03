from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import LikePost, LikeComment

class LikePostSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')

    class Meta:
        model = LikePost
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None 
        like = LikePost.objects.create(**validated_data)
        return like
        


class LikeCommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')

    class Meta:
        model = LikeComment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None 
        like = LikeComment.objects.create(**validated_data)
        return like
