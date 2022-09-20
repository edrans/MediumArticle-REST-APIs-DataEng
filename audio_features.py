import pandas as pd
from spotify_dataset_builder import Spotify

obj = Spotify()

token = obj.get_session_token(obj.clientID, obj.clientSecret)
print('Getting playlist items')
playlist_df = obj.get_playlist_items(token, obj.playlist_id)

print('Generating track list')
track_list = obj.get_track_list(playlist_df)

print('Getting audio features')
audio_features = obj.get_audio_features(token, track_list)

print('Assembling data')
playlist_audio_features = obj.join_dataframes(playlist_df, audio_features)

print('Writting files')
playlist_audio_features.to_csv('playlist_audio_features.csv', index=True)
print('Done!')
