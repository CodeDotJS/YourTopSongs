import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

scope = 'playlist-read-private'

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

limit = 50
offset = 0

playlist_data = []

while True:
    playlists = sp.current_user_playlists(limit=limit, offset=offset)

    for playlist in playlists['items']:
        if playlist['name'].startswith('Your Top Songs '):
            playlist_name = playlist['name']
            playlist_id = playlist['id']

            results = sp.playlist_tracks(playlist_id, fields='items(track(name, artists(name), id, external_urls.spotify, album(images))), total')

            tracks = results['items']
            while 'next' in results and results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])

            track_ids = [track['track']['id'] for track in tracks]

            audio_features = sp.audio_features(track_ids)

            playlist_tracks = []
            for track, audio_feature in zip(tracks, audio_features):
                track_data = track['track']
                track_name = track_data['name']
                artist_names = [artist['name'] for artist in track_data['artists']]
                track_url = track_data['external_urls']['spotify']
                cover_image = track_data['album']['images'][0]['url'] if track_data['album']['images'] else None

                track_audio_features = {
                    'duration_ms': audio_feature['duration_ms'],
                    'key': audio_feature['key'],
                    'mode': audio_feature['mode'],
                    'time_signature': audio_feature['time_signature'],
                    'acousticness': audio_feature['acousticness'],
                    'danceability': audio_feature['danceability'],
                    'energy': audio_feature['energy'],
                    'instrumentalness': audio_feature['instrumentalness'],
                    'liveness': audio_feature['liveness'],
                    'loudness': audio_feature['loudness'],
                    'speechiness': audio_feature['speechiness'],
                    'valence': audio_feature['valence'],
                    'tempo': audio_feature['tempo']
                }

                playlist_tracks.append({
                    'name': track_name,
                    'artists': artist_names,
                    'track_url': track_url,
                    'cover_image': cover_image,
                    'audio_features': track_audio_features
                })

            print("Fetching data from", playlist_name)
            playlist_data.append({'name': playlist_name, 'tracks': playlist_tracks})

    total_playlists = playlists['total']
    offset += limit

    if offset >= total_playlists:
        break

data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'playlist_data.json'))

with open(data_path, 'w') as json_file:
    json.dump(playlist_data, json_file, indent=4)

print("Saved!")
