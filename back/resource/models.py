from django.db import models



class Resource(models.Model):
    link = models.CharField(max_length=100)