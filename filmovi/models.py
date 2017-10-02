from django.contrib.auth.models import Permission, User
from django.db import models


class Film(models.Model):
    user = models.ForeignKey(User, default=1)
    reditelj = models.CharField(max_length=250)
    naziv_filma = models.CharField(max_length=500)
    godina = models.CharField(max_length=4)
    plakat = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.naziv_filma + ' - ' + self.reditelj


class Song(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    naziv_pesme = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.naziv_pesme
