from django.db import models

from django.db import connection
from django.db.utils import DatabaseError

# Create your models here.

class UserSession(models.Model):
    uid = models.IntegerField(unique=True)
    token = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    enabled = models.BooleanField()

    def __unicode__(self):
       return self.last_name + " " + self.first_name 
    
class Friend(models.Model):
    user_id = models.CharField(max_length=255)
    friend_id = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    
    @staticmethod
    def get_nomore():
        return Friend.objects.raw("SELECT * FROM face_friend WHERE friend_id NOT IN (SELECT friend_id FROM face_friendcompare)")


class FriendCompare(models.Model):
    user_id = models.CharField(max_length=255)
    friend_id = models.CharField(max_length=255)
    
    @staticmethod
    def truncate():
        cursor = connection.cursor()
        try:
            cursor.execute("TRUNCATE TABLE face_friendcompare")
        except DatabaseError:
            cursor.execute("DELETE FROM face_friendcompare")
