from django.db import models

class Skill(models.Model):
  """
  Модель для хранения названия навыка
  """

  name = models.CharField(max_length=255, unique=True)

  def __str__(self):
    return self.name