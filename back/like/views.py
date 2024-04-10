from django.shortcuts import render
from rest_framework import viewsets
from .models import Like
from .serializers import LikeSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import JWTAuthentication

class LikeViewSet(viewsets.ModelViewSet):
  queryset = Like.objects.all()
  serializer_class = LikeSerializer
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  def create(self, request):
    serializer = CreateLikeSerializer(data=request.data)
    if serializer.is_valid():
      # Get user ID from the currently logged-in user
      serializer.validated_data['user'] = request.user
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def destroy(self, request, pk):
    serializer = DeleteLikeSerializer(data=request.data)
    if serializer.is_valid():
      try:
        like = Like.objects.get(video_id=serializer.data['video_id'], user=request.user)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      except Like.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)