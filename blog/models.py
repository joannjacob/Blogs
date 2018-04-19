from django.db import models
from django.utils import timezone


class Users(models.Model):

    firstname=models.CharField(max_length=100,default="")
    lastname=models.CharField(max_length=100,default="")
    emailid=models.CharField(max_length=100,default="",unique=True)
    mobile=models.CharField(max_length=100,default="")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    security_question=models.CharField(max_length=100,default="")
    security_answer = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



class Blog(models.Model):

    user=models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title=models.CharField(max_length=100,default="")
    content=models.CharField(max_length=100,default="")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"



class Comment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,default="")
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)
    comment = models.TextField(max_length=500,default="")


    def __str__(self):
        return self.comment

class Like(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,default="")
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)

    def __str__(self):
        return self.user

