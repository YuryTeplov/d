from rest_framework import serializers
from .models import YouTubeVideo

class YouTubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = ('id', 'title', 'description', 'youtube_url', 'thumbnail_url')