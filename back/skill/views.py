from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import re
import fake_headers
from .models import Skill

def get_tags(url):
  """
  Функция для парсинга тэгов из первых 10 вакансий

  Args:
      job_title (str): Название вакансии

  Returns:
      list: Список тэгов
  """

  # Отправка GET-запроса
  headers_gen = fake_headers.Headers(os='win', browser='yandex')
  response = requests.get(url, headers=headers_gen.generate())

  # Парсинг HTML-кода
  soup = BeautifulSoup(response.content, 'html.parser')

  # Список тэгов
  tags = []

  print('111111111111')
  for tag_element in soup.find_all('span', class_='bloko-tag__section_text'):
    tag = tag_element.text
    tags.append(tag)

  # Очистка и удаление дубликатов
  tags = [tag.lower().strip() for tag in tags]
  tags = set(tags)

  return tags

def has_vacancy(string):
  """
  Функция для проверки наличия "/vacancy/" в строке

  Args:
      string (str): Входная строка

  Returns:
      bool: True, если "/vacancy/" найдено, False - в противном случае
  """

  return "/vacancy/" in string.lower()

# Функция для получения списка вакансий по названию профессии
def get_vacancies(job_title):
  """
  Функция, которая на входе принимает текст с названием профессии, а на выходе возвращает список вакансий

  Args:
      job_title (str): Текст с названием профессии

  Returns:
      list: Список вакансий
  """

  url = "https://hh.kz/search/vacancy?text="+ job_title +"&area=159&hhtmFrom=main&hhtmFromLabel=vacancy_search_line"

  headers_gen = fake_headers.Headers(os='win', browser='yandex')
  response = requests.get(url, headers=headers_gen.generate())
  print(response)

  if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    skills = []

    for link in soup.find_all('a', class_='bloko-link'):
        vacancy_link = link['href']
        if has_vacancy(vacancy_link): 
            skills.append(get_tags(vacancy_link))
    return skills
  else:
    raise Exception("Ошибка при запросе к HeadHunter: " + str(response.status_code))


def get_skills_for_profession(request, search):
    try: 
        # Пример использования
        skills = get_vacancies(search)

        # Сохранение новых навыков в базе данных
        for skill_name in skills:
            skill, created = Skill.objects.get_or_create(name=skill_name)
            if created:
                print(f"Сохранен новый навык: {skill_name}")

        return JsonResponse(skills)
    except: 
        return JsonResponse({'error': 'error'})