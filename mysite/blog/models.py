from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.name

class Post(models.Model):
    pub_date = models.DateTimeField('Published')
    content = models.TextField()
    title = models.CharField(max_length = 300)
    category = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.title

    
