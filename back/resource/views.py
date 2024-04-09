from django.shortcuts import render
from .utils import search_youtube_videos
from skill.models import Skill


def load_videos_by_skill(request, skill):
    # Поиск видео
    videos = search_youtube_videos(skill_name)

    # Получение объекта Skill
    skill = Skill.objects.get(name=skill_name)

    # Добавление видео в базу данных
    add_videos_to_database(videos, skill)