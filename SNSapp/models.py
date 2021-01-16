from django.db import models

class SnsModel(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    author = models.CharField(max_length=100,null=True,blank=True)
    readtext = models.CharField(max_length=200,null=True,blank=True)
    good = models.IntegerField(null=True, blank=True, default=0)
    read = models.IntegerField(null=True, blank=True, default=0)
    images = models.ImageField(upload_to='',null=True,blank=True)
    content = models.TextField(null=True,blank=True)
