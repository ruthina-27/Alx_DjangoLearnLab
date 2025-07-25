# NOTE: The custom user model (CustomUser) is NOT defined in this file.
# It is implemented in advanced_features_and_security/accounts/models.py as per project requirements.
from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
