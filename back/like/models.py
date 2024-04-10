from django.db import models
from resource.models import YouTubeVideo
from django.contrib.auth import get_user_model

class Like(models.Model):
  video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE)
  user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = (("video", "user"),)
