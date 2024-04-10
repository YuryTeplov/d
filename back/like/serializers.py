from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = ('id', 'video', 'user', 'timestamp')

class CreateLikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = ('video_id', 'user_id')

class DeleteLikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = ('video_id', 'user_id')