from django.shortcuts import render,redirect
from .forms import SongForm
from .models import Song
import random
from sklearn.neighbors import KNeighborsClassifier
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id=open('spotify_client_id.txt')
client_secret=open('spotify_client_secret.txt')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,client_secret=client_secret))  #spotify api

def home(request):
    return render(request, 'home.html')

#using the api classify the genre
def classify_genre(song_title,artist):

    results = sp.search(q=f'track:{song_title} artist:{artist}', type='track', limit=1) #dictionary  

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

    results = sp.recommendations(seed_genres=[genre], limit=5) #results is a dictionary having tracks and seeds as keys
    similar_songs = []

    for track in results['tracks']:

        similar_songs.append({
            'title': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'genre': genre
        })

    return similar_songs

#main function
def classify_song(request):

    if request.method=='POST':
        form=SongForm(request.POST)

        if form.is_valid():

            song=form.save(commit=False) # false so that before adding the song, genre is identified
            genre = classify_genre(song.title,song.artist) #to get the genre
            song.genre=genre
            #genre field is set dynamically after form submission
            #if commit=False is removed, an incomplete object is formed and would result in an error while saving to database
            song.save()

            similar_songs = recommend_similar_songs(genre) 

            return render(request, 'songs/result.html', {'song': song, 'similar_songs': similar_songs})
    else:
        form = SongForm()

    return render(request, 'songs/classify.html', {'form': form})

'''
recommendations: parameters: genre,artist,tracks(any 1 must be provided); limit country(optional)
response: tracks(key): name,id,artists,album,popularity,tracks uri (all values)

search: parameters: query string(q)-artist/track/album, limit(optional)
'''