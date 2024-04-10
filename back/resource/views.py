from django.shortcuts import render
from .utils import search_youtube_videos, add_videos_to_database
from skill.models import Skill
from django.http import JsonResponse


def load_videos_by_skill(request, skill_name):
    # Поиск видео
    videos = search_youtube_videos(skill_name)

    # Получение объекта Skill
    skill = Skill.objects.get(name=skill_name)

    # Добавление видео в базу данных
    add_videos_to_database(videos, skill)

    resp = JsonResponse({'videos': videos}, charset='utf-8')

    return resp