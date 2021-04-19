from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#アプリ内のユーザーtable
class AppUsers(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    age = models.IntegerField(null=True, blank=True, default=0)
    images = models.ImageField(upload_to='',null=True,blank=True)
    company = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    #セレクトボックスでもいいかも
    hoby = models.CharField(max_length=100,null=True,blank=True)
    #出身地は選択で選ぶ
    birthplace = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=100,null=True,blank=True)
    introduction = models.TextField(max_length=1000,null=True,blank=True)

#投稿table
class SnsModel(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    author = models.CharField(max_length=100,null=True,blank=True)
    readtext = models.CharField(max_length=200,null=True,blank=True)
    good = models.IntegerField(null=True, blank=True, default=0)
    read = models.IntegerField(null=True, blank=True, default=0)
    images = models.ImageField(upload_to='',null=True,blank=True)
    content = models.TextField(max_length=500,null=True,blank=True)
    user = models.ForeignKey(AppUsers,null=True,blank=True,on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)

#フォローtable
class Follow(models.Model):
    user = models.ForeignKey(AppUsers,null=True,blank=True,on_delete=models.CASCADE,related_name='follow_user')
    user_2 = models.ForeignKey(AppUsers,null=True,blank=True,on_delete=models.CASCADE,related_name='followed_user')
    shonin_status = models.IntegerField(null=True, blank=True,  default=0)


class Coment(models.Model):
    comment = models.TextField(max_length=1000,null=True,blank=True)
    #コメントを投稿したユーザー
    comment_user = models.ForeignKey(AppUsers,null=True,blank=True,on_delete=models.CASCADE,related_name='comment_user')
    #投稿主ユーザー
    user = models.ForeignKey(AppUsers,null=True,blank=True,on_delete=models.CASCADE,related_name='sns_user')