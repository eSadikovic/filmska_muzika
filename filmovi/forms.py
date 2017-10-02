from django import forms
from django.contrib.auth.models import User

from .models import Film, Song


class FilmForm(forms.ModelForm):

    class Meta:
        model = Film
        fields = ['reditelj', 'naziv_filma', 'godina', 'plakat']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['naziv_pesme', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
