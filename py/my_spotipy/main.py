import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope="user-library-read user-top-read"
))


def test1():
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])


def test2():
    results = sp.current_user_top_tracks(time_range='short_term', limit=10)
    tracks_info = []

    # Iteracja przez utwory i zbieranie danych
    for item in results['items']:
        track = {
            'Tytuł': item['name'],
            'Artysta': ', '.join(artist['name'] for artist in item['artists']),  # Może być więcej niż jeden artysta
            'Album': item['album']['name'],
            'Data wydania': item['album']['release_date'],
            'Popularność': item['popularity'],
            'Czas trwania': f"{item['duration_ms'] // 60000}:{str(item['duration_ms'] % 60000).zfill(2)}",  # Zamiana milisekund na minuty i sekundy
            'Długość (ms)': item['duration_ms'],
            'Tempo': item['tempo'],
            'Tonacja': item['key'],
            'Tryb': 'Moll' if item['mode'] == 0 else 'Durowy',
            'Energia': item['energy'],
            'Taneczność': item['danceability'],
            'Głośność': item['loudness'],
            'Akustyczność': item['acousticness'],
            'Instrumentalność': item['instrumentalness'],
            'Żywiołowość': item['liveness'],
            'Nastrojowość': item['valence'],
            'Spójność': item['speechiness'],
            'ID Utworu': item['id'],
            'Link do Spotify': item['external_urls']['spotify']
        }
        tracks_info.append(track)

    # Tworzenie DataFrame'u z listy
    df_tracks = pd.DataFrame(tracks_info)

    # Wyświetlenie DataFrame'u
    print(df_tracks)

    # Eksport DataFrame'u do pliku CSV
    df_tracks.to_csv('top_tracks.csv', index=False)


test2()
