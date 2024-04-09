from django.db import models

class YouTubeVideo(models.Model):
  """
  Модель для хранения информации о видео на YouTube
  """

  title = models.CharField(max_length=255)
  description = models.TextField()
  youtube_url = models.URLField()

  def __str__(self):
    return self.title

from skill.models import Skill

class VideoSkill(models.Model):
  """
  Модель связи между видео и навыками
  """

  video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE)
  skill = models.ForeignKey(Skill, on_delete=models.CASCADE)