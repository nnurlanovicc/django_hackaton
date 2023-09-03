from rest_framework.serializers import ModelSerializer,  ReadOnlyField
from .models import Comment
from apps.like.models import LikeComment
from apps.like.serializers import LikeCommentSerializer

class CommentSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        comment = Comment.objects.create(**validated_data)
        return comment        


    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['likes'] = LikeCommentSerializer(LikeComment.objects.filter(post=instance.pk), many=True).data
    #     return representation