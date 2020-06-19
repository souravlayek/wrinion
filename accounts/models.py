from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='images/')
    interest = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class FriendManager(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='first_user')
    second_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='second_user')
    approval = models.BooleanField(default=False)

    def __str__(self):
        friend = f"{self.first_user}{self.second_user}"
        return friend