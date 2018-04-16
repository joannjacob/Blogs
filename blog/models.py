from django.db import models
from django.utils import timezone


class User(models.Model):

    firstname=models.CharField(max_length=100,default="")
    lastname=models.CharField(max_length=100,default="")
    emailid=models.CharField(max_length=100,default="",unique=True)
    mobile=models.CharField(max_length=100,default="")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    security_question=models.CharField(max_length=100,default="")
    security_answer = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return '%s %s %s %s'%(self.username,self.password,
                              self.security_question,self.security_answer)

class Blog(models.Model):

    user= models.ForeignKey('User',on_delete=models.CASCADE)
    email=models.CharField(max_length=100,default="")
    title=models.CharField(max_length=100,default="")
    content=models.CharField(max_length=500,default="")

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"

    def __str__(self):
        return '%s %s'(self.content,self.title)

class Comment(models.Model):

    post = models.ForeignKey('Blog',on_delete=models.CASCADE)
    text = models.TextField()
    author = models.CharField(max_length=100)

    def __str__(self):
        return "[%s] %s" % (self.author, self.text)

class Like(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    content = models.ForeignKey(Blog)
    timestamp = models.DateTimeField()

    def __str__(self):
        return '%s %s'(self.User.username)