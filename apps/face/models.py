from django.db import models

# Create your models here.

class UserSession(models.Model):
    uid = model.IntegerField()
    token model.CharField(max_length=255)
