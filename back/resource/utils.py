from googleapiclient.discovery import build
import requests
import fake_headers
from bs4 import BeautifulSoup

# Модели
from .models import YouTubeVideo, VideoSkill
import os

def get_course_data(search_string):
  """
  Функция парсит данные курса с URL-адреса.

  Args:
    url (str): URL-адрес страницы курса.

  Returns:
    dict: Словарь с информацией о курсе, 
         включая название, описание, изображение и ссылку.
  """

  headers_gen = fake_headers.Headers(os='win', browser='yandex')

  response = requests.get('https://www.coursera.org/search?query='+search_string, headers=headers_gen)
  soup = BeautifulSoup(response.content, 'lxml')

  course_title = soup.find('h2', class_='title').text.strip()
  course_description = soup.find('div', class_='description').text.strip()
  course_image = soup.find('img', class_='card-img-top')['src']
  course_link = url

  return {
      'title': course_title,
      'description': course_description,
      'image': course_image,
      'link': course_link
  }

def get_courses(url):
  """
  Функция парсит список курсов с URL-адреса.

  Args:
    url (str): URL-адрес страницы с курсами.

  Returns:
    list: Список словарей с информацией о курсах.
  """
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'lxml')

  courses = []
  for course_card in soup.find_all('div', class_='card'):
    course_url = course_card.find('a')['href']
    course_data = get_course_data(course_url)
    courses.append(course_data)

  return courses


# API YouTube
API_KEY = os.getenv('YOUTUBE_API_KEY', '') 

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
    maxResults=100,
  )

  response = request.execute()


  videos = []

  for video in response["items"]:
    if video["id"]["kind"] == "youtube#video" and video["id"]["videoId"]:
      thumbnail_url = video["snippet"]["thumbnails"]["default"]["url"] 
      videos.append({
        "title": video["snippet"]["title"],
        "description": video["snippet"]["description"],
        "youtube_url": "https://www.youtube.com/watch?v=" + video["id"]["videoId"],
        "thumbnail_url": thumbnail_url,
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
      thumbnail_url=video["thumbnail_url"],
    )

    if created:
      print(f"Сохранено новое видео: {video['title']}")

    # Связь видео с навыком
    VideoSkill.objects.get_or_create(video=youtube_video, skill=skill)