from django.db import models

# Create your models here.

class UserSession(models.Model):
    uid = models.IntegerField(unique=True)
    token = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    enabled = models.BooleanField()

    def __unicode__(self):
       return self.last_name + " " + self.first_name 

class Friends(models.Model):
    user_id = models.ForeignKey('UserSession')
    friend_id = models.IntegerField()
