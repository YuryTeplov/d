from googleapiclient.discovery import build

# Модели
from .models import YouTubeVideo, VideoSkill

# API YouTube
API_KEY = "YOUR_API_KEY"

def search_youtube_videos(skill_name):
  """
  Функция поиска видео на YouTube по названию навыка

  Args:
      skill_name (str): Название навыка

  Returns:
      list: Список словарей с информацией о видео
  """

  youtube = build("youtube", "v3", developerKey=API_KEY)

  request = youtube.search().list(
    part="snippet",
    q=skill_name,
    maxResults=10,
  )

  response = request.execute()

  videos = []

  for video in response["items"]:
    videos.append({
      "title": video["snippet"]["title"],
      "description": video["snippet"]["description"],
      "youtube_url": "https://www.youtube.com/watch?v=" + video["id"]["videoId"],
    })

  return videos

def add_videos_to_database(videos, skill):
  """
  Функция добавления видео в базу данных

  Args:
      videos (list): Список словарей с информацией о видео
      skill (Skill): Объект модели Skill

  Returns:
      None
  """

  for video in videos:
    youtube_video, created = YouTubeVideo.objects.get_or_create(
      title=video["title"],
      description=video["description"],
      youtube_url=video["youtube_url"],
    )

    if created:
      print(f"Сохранено новое видео: {video['title']}")

    # Связь видео с навыком
    VideoSkill.objects.get_or_create(video=youtube_video, skill=skill)