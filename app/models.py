from email.policy import default
import imp
import profile
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


class ProfileManager(models.Manager):
    pass

class Profile(models.Model):
    avatar = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}"
    pass

class TagManager(models.Manager):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=32)
    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    pass


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)

    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    object = QuestionManager()


class AnswerManager(models.Manager):
    pass


class Answer(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    correct = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    objects = AnswerManager()




class LikeQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class LikeAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    





