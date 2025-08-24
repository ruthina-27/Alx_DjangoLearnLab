from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # following: users that this user follows
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow a user"""
        if user != self:
            self.following.add(user)
    
    def unfollow(self, user):
        """Unfollow a user"""
        self.following.remove(user)
    
    def is_following(self, user):
        """Check if this user is following another user"""
        return self.following.filter(id=user.id).exists()
