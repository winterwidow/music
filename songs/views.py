from django.shortcuts import render,redirect
from .forms import SongForm
from .models import Song
import random
from sklearn.neighbors import KNeighborsClassifier
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='6743d0e5040a4100b74091667f3a8991',client_secret='2608e96d0a1a4d6e912fb9a6482510c7'))  #spotify api

def home(request):
    return render(request, 'home.html')

#using the api classify the genre
def classify_genre(song_title,artist):
    results = sp.search(q=f'track:{song_title} artist:{artist}', type='track', limit=1) #using the api to search for songs 

    if results['tracks']['items']:

        track=results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        genre = artist_info['genres'][0] if artist_info['genres'] else 'Unknown'
        return genre
    else:
        return 'Unknown'
    
#use the spotify api to generate similar songs
def recommend_similar_songs(genre):
    results = sp.recommendations(seed_genres=[genre], limit=5) #using spotify api
    similar_songs = []

    for track in results['tracks']:

        similar_songs.append({
            'title': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'genre': genre
        })
    return similar_songs

def classify_song(requests):
    if request.method=='POST':
        form=SongForm(request.POST)
        if form.is_valid():
            song=form.save(commit=False)
            genre = classify_genre(song.title,song.artist)
            song.genre=genre
            song.save()

            similar_songs = recommend_similar_songs(genre)
            return render(request, 'songs/result.html', {'song': song, 'similar_songs': similar_songs})
    else:
        form = SongForm()
    return render(request, 'songs/classify.html', {'form': form})