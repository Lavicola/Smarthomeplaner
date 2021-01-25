from django.db import models
from django.contrib.auth import settings

# Create your models here.

class CanvasMap(models.Model):
    email = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True)
    canvas_map = models.JSONField()