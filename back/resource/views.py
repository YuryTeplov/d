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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict, Counter

def get_video_description(video_id):
  """
  Fetches the description for a YouTube video from the database.

  Args:
      video_id: The ID of the YouTube video stored in your database.

  Returns:
      The description of the YouTube video from the database, or None if not found.
  """

  try:
    # Get the YouTubeVideo object from the database
    video = YouTubeVideo.objects.get(pk=video_id)
    return video.description

  except YouTubeVideo.DoesNotExist:
    print(f"Video with ID {video_id} not found in the database")
    return None

  except Exception as e:
    print(f"Error fetching video description for ID {video_id}: {e}")
    return None

  return None

def calculate_user_similarities(liked_videos):
  user_similarities = defaultdict(dict)
  for user_id, main_liked_videos in liked_videos.items():
    if isinstance(liked_videos, dict):
      for other_user_id, other_liked_videos in liked_videos.items():
        if user_id != other_user_id:
          intersection = set(main_liked_videos) & set(other_liked_videos)
          user_similarities[user_id][other_user_id] = len(intersection)
    else:
      print("liked_videos is not a dictionary. Recommendations might not be accurate.")
  return user_similarities

def recommend_videos(liked_videos, user_similarities, skill_videos, current_user_id, k=5):

  cbf_recommendations = recommend_videos_cbf(liked_videos, skill_videos, current_user_id, len(skill_videos))

  recommendations = defaultdict(list)
  for user_id, main_liked_videos in liked_videos.items():
    for similar_user_id, similarity in user_similarities[user_id].items():
      if similar_user_id != user_id:
        for video_id in liked_videos[similar_user_id]:
          if video_id not in liked_videos[user_id] and video_id not in recommendations[user_id]:
            recommendations[user_id].append(video_id)
    # Sort recommendations by similarity score (higher score first)
    recommendations[user_id].sort(key=lambda video_id: similarity, reverse=True)

  counter_of_recs = Counter(recommendations[current_user_id])

  for skill_video in cbf_recommendations:
    skill_video["similarity_score_cf"] = counter_of_recs[skill_video["id"]/len(user_similarities)]


  # Sort combined recommendations by similarity scores (CF first)
  cbf_recommendations.sort(key=lambda video: 0.7 * video["similarity_score_cf"] + 0.3 * video["similarity_score_cbf"], reverse=True)

  return cbf_recommendations


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
    courses = get_course_data(skill_name)

    print(courses)


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

def recommend_videos_cbf(liked_videos, skill_videos, current_user_id, k=3):
  # Extract descriptions from liked videos
  liked_video_descriptions = []
  for user_id, liked_video_ids in liked_videos.items():
    if user_id == current_user_id:
      for video_id in liked_video_ids:
        video_description = get_video_description(video_id)  # Assuming get_video_description fetches descriptions
        liked_video_descriptions.append(video_description)

  # Represent video descriptions using TF-IDF
  vectorizer = TfidfVectorizer()
  liked_video_descriptions_matrix = vectorizer.fit_transform(liked_video_descriptions)
  video_descriptions_matrix = vectorizer.transform([video["description"] for video in skill_videos])

  # Calculate cosine similarity between liked and all videos
  similarities = cosine_similarity(liked_video_descriptions_matrix, video_descriptions_matrix)

  # Convert the similarities matrix to a 1D array
  flattened_similarities = similarities.ravel()

  # Create an array to store the maximum similarity for each video in skill_videos
  max_similarities = np.zeros(len(skill_videos))

  for i in range(len(skill_videos)):
    start_index = i * liked_video_descriptions_matrix.shape[0]
    end_index = start_index + liked_video_descriptions_matrix.shape[0]

    # Calculate the average of the slice
    slice_sum = sum(flattened_similarities[start_index:end_index])
    avg = slice_sum / (end_index - start_index)

    # Assign the average to the similarity_score_cbf key
    skill_videos[i]["similarity_score_cbf"] = avg

  return skill_videos


class VideoViewSet(viewsets.ModelViewSet):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]
  queryset = YouTubeVideo.objects.all()  # Define the queryset here
  serializer_class = YouTubeVideoSerializer  # Assuming you have a VideoSerializer
  # ... other viewset methods

  def load_videos_by_skill(self, request, skill_name):
    skill_videos = get_videos(skill_name)  # Assuming get_videos filters by skill

    serializer = YouTubeVideoSerializer(skill_videos, many=True)
    videos_data = serializer.data

    liked_videos = {}
    for like in Like.objects.all():
      liked_videos.setdefault(like.user_id, []).append(like.video_id)

    user_similarities = calculate_user_similarities(liked_videos)

    recommended_videos = recommend_videos(liked_videos, user_similarities, videos_data, current_user_id=request.user.id, k=3)  # Adjust k as needed


    for video in recommended_videos:
        video['liked'] = Like.objects.filter(video_id=video['id'], user_id=request.user.id).exists()

    if len(recommended_videos) > 0:
      return recommended_videos
    else:

      for video in videos_data:
        video['liked'] = Like.objects.filter(video_id=video['id'], user_id=request.user.id).exists()
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

