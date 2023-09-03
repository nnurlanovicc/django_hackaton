from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from .models import Post
from apps.comment.models import Comment
from apps.comment.serializers import CommentSerializer
from apps.like.models import LikePost
from apps.like.serializers import LikePostSerializer


class ValidationMixin:
    def validate_title(self, title):
        if self.Meta.model.objects.filter(title=title).exists():
            raise ValidationError('такое название уже существует')
        return title
class PostDetailSerializer(ValidationMixin, ModelSerializer):
    author = ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(author=user, **validated_data)
        post.tags.add(*tags)
        return post
    


class PostListSerializer(ValidationMixin, ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(Comment.objects.filter(post=instance.pk), many=True).data
        representation['likes'] = LikePostSerializer(LikePost.objects.filter(post=instance.pk), many=True).data
        return representation

