from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer, CreateLikeSerializer, DeleteLikeSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class LikeViewSet(viewsets.ModelViewSet):
  queryset = Like.objects.all()
  serializer_class = LikeSerializer
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  def create(self, request):

    serializer = CreateLikeSerializer(data=request.data)
    print(serializer.initial_data)
    serializer.is_valid(raise_exception=True)  # Raise exception for invalid data

    # Get user ID from the currently logged-in user (assuming request.user is valid)
    serializer.validated_data['user_id'] = request.user.id

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def destroy(self, request, pk=None):
    # Handle case where pk is not provided
    if not pk:
      return Response({'error': 'Missing video ID in request'}, status=status.HTTP_400_BAD_REQUEST)

    # No need for DeleteLikeSerializer, use pk directly
    try:
      like = Like.objects.get(video_id=pk, user_id=request.user.id)  # Assuming pk is the video_id
      like.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)