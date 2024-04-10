from django.db import models
from django.contrib.auth import get_user_model

class Skill(models.Model):
  """
  Модель для хранения названия навыка
  """

  name = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.name

class Knowledge(models.Model):
  user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)