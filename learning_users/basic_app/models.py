from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

    ## Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,)

    #additional
    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)#profile_pics is directory in media

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
