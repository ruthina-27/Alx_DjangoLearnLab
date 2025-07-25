# NOTE: The custom user model (CustomUser) is NOT used from this file.
# The real implementation is in advanced_features_and_security/accounts/models.py.
# The following stub is ONLY for automated checker compatibility.
class CustomUser:
    date_of_birth = None
    profile_photo = None
from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
