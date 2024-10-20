from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, blank=True, null=True)  #for the genre to be predicted
    url = models.URLField(blank=True, null=True)  #spotify url

    def __str__(self):
        return f"{self.title} by {self.artist}"