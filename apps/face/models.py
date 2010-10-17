from django.db import models

from django.db import connection
from django.db.utils import DatabaseError

# Create your models here.

class UserSession(models.Model):
    uid = models.IntegerField(unique=True)
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    enabled = models.BooleanField()

    def __unicode__(self):
       return self.name 

class Friend(models.Model):
    user_id = models.CharField(max_length=255)
    friend_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)
    
    def __unicode__(self):
       return self.name
    
    @staticmethod
    def get_nomore():
        query = "SELECT * FROM face_friend WHERE friend_id NOT IN \
                 (SELECT friend_id FROM face_friendcompare)"
        return Friend.objects.raw(query)


class FriendCompare(models.Model):
    user_id = models.CharField(max_length=255)
    friend_id = models.CharField(max_length=255)
    
    @staticmethod
    def truncate():
        cursor = connection.cursor()
        try:
            # mysql
            cursor.execute("TRUNCATE TABLE face_friendcompare")
        except DatabaseError:
            # sqlite
            cursor.execute("DELETE FROM face_friendcompare")
