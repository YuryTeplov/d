from django.shortcuts import render
from .utils import search_youtube_videos, add_videos_to_database
from skill.models import Skill
from django.http import JsonResponse
from .models import YouTubeVideo, VideoSkill
from .serializers import YouTubeVideoSerializer
from like.models import Like
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from collections import defaultdict

def calculate_user_similarities(liked_videos):
  user_similarities = defaultdict(dict)
  for user_id, liked_videos in liked_videos.items():
    if isinstance(liked_videos, dict):
      for other_user_id, other_liked_videos in liked_videos.items():
        if user_id != other_user_id:
          intersection = set(liked_videos) & set(other_liked_videos)
          user_similarities[user_id][other_user_id] = len(intersection)
    else:
      '''
      for liked_video in liked_videos:
        # Extract user ID and liked video ID from each element in the list
        user_id = liked_video['user_id']  # Assuming user ID field in the list element
        video_id = liked_video['video_id']  # Assuming video ID field

        # Update your logic to process individual liked videos (e.g., add them to a dictionary)
        liked_videos_dict.setdefault(user_id, []).append(video_id)
      '''
      print("liked_videos is not a dictionary. Recommendations might not be accurate.")
  return user_similarities

def recommend_videos(liked_videos, user_similarities, videos, k=5):
  recommendations = defaultdict(list)
  for user_id, liked_videos in liked_videos.items():
    for similar_user_id, similarity in user_similarities[user_id].items():
      if similar_user_id != user_id:
        for video_id in liked_videos[similar_user_id]:
          if video_id not in liked_videos[user_id] and video_id not in recommendations[user_id]:
            recommendations[user_id].append(video_id)
    # Sort recommendations by similarity score (higher score first)
    recommendations[user_id].sort(key=lambda video_id: similarity, reverse=True)
    # Take the top k recommendations
    recommendations[user_id] = recommendations[user_id][:k]

  recommended_videos = []
  for user_id, video_ids in recommendations.items():
    for video_id in video_ids:
      recommended_videos.append(get_video(video_id))  # Assuming get_video fetches video details

  return recommended_videos


def get_videos(skill_name):
  """
  Функция получает видео с YouTube для указанного навыка.

  Args:
    skill_name: Название навыка.

  Returns:
    Список объектов YouTubeVideo.
  """

  # Получение навыка
  skill = Skill.objects.get(name=skill_name)

  # Получение связанных видео
  youtube_videos = YouTubeVideo.objects.filter(videoskill__skill=skill)

  # Если видео не найдены, поиск на YouTube
  if not youtube_videos:
    # Получение видео с YouTube
    youtube_videos = search_youtube_videos(skill_name)


    # Сохранение видео в базе данных
    for video in youtube_videos:
      new_video = YouTubeVideo(title=video["title"],
                                description=video["description"],
                                youtube_url=video["youtube_url"],
                                thumbnail_url=video["thumbnail_url"],
                                )
      new_video.save()

      # Связь видео с навыком
      VideoSkill.objects.create(video=new_video, skill=skill)


  return youtube_videos

class VideoViewSet(viewsets.ModelViewSet):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  queryset = YouTubeVideo.objects.all()  # Define the queryset here
  serializer_class = YouTubeVideoSerializer  # Assuming you have a VideoSerializer
  # ... other viewset methods

  def load_videos_by_skill(self, request, skill_name):
    skill_videos = get_videos(skill_name)  # Assuming get_videos filters by skill

    liked_videos = {}
    for like in Like.objects.filter(user_id=request.user.id):
        liked_videos.setdefault(like.user_id, []).append(like.video_id)

    user_similarities = calculate_user_similarities(liked_videos)
    recommended_videos = recommend_videos(liked_videos, user_similarities, k=3)  # Adjust k as needed

    serializer = YouTubeVideoSerializer(skill_videos, many=True)
    videos_data = serializer.data

    for video in videos_data:
        video['liked'] = Like.objects.filter(video_id=video['id'], user_id=request.user.id).exists()

    # Add recommended videos to the response (assuming 'recommendations' key in serializer)
    videos_data['recommendations'] = YouTubeVideoSerializer(recommended_videos, many=True).data

    return videos_data

  def retrieve(self, request, pk=None):
    # Check if a skill name is provided in the query parameters
    skill_name = request.query_params.get('skill_name')

    if skill_name:
      # Use load_videos_by_skill if skill name is provided
      videos = self.load_videos_by_skill(request, skill_name)
      resp = JsonResponse({'videos': videos}, charset='utf-8')
      return resp
    else:
      return Response(status.HTTP_400_BAD_REQUEST)

