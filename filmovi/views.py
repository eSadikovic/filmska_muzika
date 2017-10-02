from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import FilmForm, SongForm, UserForm
from .models import Film, Song

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_film(request):
    if not request.user.is_authenticated():
        return render(request, 'filmovi/login.html')
    else:
        form = FilmForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            film = form.save(commit=False)
            film.user = request.user
            film.plakat = request.FILES['plakat']
            file_type = film.plakat.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'film': film,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'filmovi/create_film.html', context)
            film.save()
            return render(request, 'filmovi/detail.html', {'film': film})
        context = {
            "form": form,
        }
        return render(request, 'filmovi/create_film.html', context)


def create_song(request, film_id):
    form = SongForm(request.POST or None, request.FILES or None)
    film = get_object_or_404(Film, pk=film_id)
    if form.is_valid():
        films_songs = film.song_set.all()
        for s in films_songs:
            if s.naziv_pesme == form.cleaned_data.get("naziv_pesme"):
                context = {
                    'film': film,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'filmovi/create_song.html', context)
        song = form.save(commit=False)
        song.film = film
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'film': film,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'filmovi/create_song.html', context)

        song.save()
        return render(request, 'filmovi/detail.html', {'film': film})
    context = {
        'film': film,
        'form': form,
    }
    return render(request, 'filmovi/create_song.html', context)


def delete_film(request, film_id):
    film = Film.objects.get(pk=film_id)
    film.delete()
    films = Film.objects.filter(user=request.user)
    return render(request, 'filmovi/index.html', {'films': films})


def delete_song(request, film_id, song_id):
    film = get_object_or_404(Film, pk=film_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'filmovi/detail.html', {'film': film})


def detail(request, film_id):
    if not request.user.is_authenticated():
        return render(request, 'filmovi/login.html')
    else:
        user = request.user
        film = get_object_or_404(Film, pk=film_id)
        return render(request, 'filmovi/detail.html', {'film': film, 'user': user})

def favoritefilm(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    try:
        if film.is_favorite:
            film.is_favorite = False
        else:
            film.is_favorite = True
        film.save()
    except (KeyError, Film.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'filmovi/login.html')
    else:
        films = Film.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            films = films.filter(
                Q(naziv_filma__icontains=query) |
                Q(reditelj__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(naziv_pesme__icontains=query)
            ).distinct()
            return render(request, 'filmovi/index.html', {
                'films': films,
                'songs': song_results,
            })
        else:
            return render(request, 'filmovi/index.html', {'films': films})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'filmovi/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                films = Film.objects.filter(user=request.user)
                return render(request, 'filmovi/index.html', {'films': films})
            else:
                return render(request, 'filmovi/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'filmovi/login.html', {'error_message': 'Invalid login'})
    return render(request, 'filmovi/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                films = Film.objects.filter(user=request.user)
                return render(request, 'filmovi/index.html', {'films': films})
    context = {
        "form": form,
    }
    return render(request, 'filmovi/register.html', context)


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'filmovi/login.html')
    else:
        try:
            song_ids = []
            for film in Film.objects.filter(user=request.user):
                for song in film.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Film.DoesNotExist:
            users_songs = []
        return render(request, 'filmovi/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })
