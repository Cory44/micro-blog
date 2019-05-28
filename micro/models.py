from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import os


# Create your models here.
class User(AbstractUser):
    display_name = models.CharField(max_length=50, default=1, blank=False, null=False)

    def __str__(self):
        return (f"{self.username}")

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.display_name = self.username
            self.username = self.username.lower()
        super(self.__class__, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    published = models.DateTimeField('date published', default=datetime.now)

    def __str__(self):
        return f"{self.user.username}'s  post {self.id}"


def get_image_path(instance, filename):
    fileType = filename.split(".")
    newFilename = str(instance.user.username) + "." + fileType[len(fileType)-1]
    return os.path.join('users', newFilename)


class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    follows = models.ManyToManyField('UserProfile', related_name='followed_by', blank=True)
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"

        
