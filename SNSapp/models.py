from django.db import models

class SnsModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    images = models.ImageField(upload_to='')
    good = models.IntegerField()
    read = models.IntegerField()
    readtext = models.CharField(max_length=200)
