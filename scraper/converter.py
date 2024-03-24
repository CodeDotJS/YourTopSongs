import pandas as pd
import json
import sqlite3

with open('../data/playlist_data.json') as f:
    data = json.load(f)

tracks_list = []
for playlist in data:
    for track in playlist['tracks']:
        track_info = {
            'playlist_name': playlist['name'],
            'track_name': track['name'],
            'artist': ', '.join(track['artists']),
            'duration_ms': track['audio_features']['duration_ms'],
            'key': track['audio_features']['key'],
            'mode': track['audio_features']['mode'],
            'time_signature': track['audio_features']['time_signature'],
            'acousticness': track['audio_features']['acousticness'],
            'danceability': track['audio_features']['danceability'],
            'energy': track['audio_features']['energy'],
            'instrumentalness': track['audio_features']['instrumentalness'],
            'liveness': track['audio_features']['liveness'],
            'loudness': track['audio_features']['loudness'],
            'speechiness': track['audio_features']['speechiness'],
            'valence': track['audio_features']['valence'],
            'tempo': track['audio_features']['tempo'],
            'url': track['track_url'],
            'cover': track['cover_image']
        }
        tracks_list.append(track_info)

df = pd.DataFrame(tracks_list)
df.to_csv('../data/playlist.csv', index=False)

conn = sqlite3.connect('../data/playlist.db')
df.to_sql('playlist', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
