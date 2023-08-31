from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Like

class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.username')

    class Meta:
        model = Like
        fields = '__all__'

