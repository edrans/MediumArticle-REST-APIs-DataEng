import requests
import base64
import pandas as pd



class Spotify:
    def __init__(self):
        self.clientID = ""
        self.clientSecret = ""
        self.playlist_id = '3SHuiyj8uSGx13orS6FxEA'
        
    def get_session_token(self, clientID, clientSecret):
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}
        raw_cred = f"{clientID}:{clientSecret}"
        encoded_cred = raw_cred.encode('ascii')
        base64_cred = base64.b64encode(encoded_cred)
        auth_message = base64_cred.decode('ascii')

        headers['Authorization'] = f"Basic {auth_message}"
        data['grant_type'] = "client_credentials"

        r = requests.post(url, headers=headers, data=data)

        token = r.json()['access_token']
        return(token)
    
    def get_playlist_items(self, token, playlist_id):
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=items(track(name, album.name, artists.name, id))"
        payload={}
        headers = {
         "Authorization": "Bearer " + str(token)
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        playlist_df = pd.json_normalize(response.json().get('items'))
        playlist_df.rename(columns={"track.album.name": "album", "track.artists": "artist", "track.id":"id", "track.name":"name" }, inplace = True)
        playlist_df = playlist_df[['id','name','artist','album']]
        for i in range (0,len(playlist_df['artist'])):
            playlist_df['artist'][i] = playlist_df['artist'][i][0].get('name')
        return (playlist_df)
    
    def get_track_list(self, playlist_df):
        track_ids = tuple(list(playlist_df['id']))
        track_ids = ','.join(track_ids)
        track_ids = track_ids.replace("'", "")
        return (track_ids)

    def get_audio_features(self, token, track_ids):
        url = f"https://api.spotify.com/v1/audio-features?ids={track_ids}"
        payload={}
        headers = {
         "Authorization": "Bearer " + str(token)
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        audio_features = pd.json_normalize(response.json().get('audio_features'))
        return (audio_features)

    def join_dataframes (self, playlist_df, audio_features):
        playlist_features = pd.merge(playlist_df,
                                     audio_features,
                                     how="inner",
                                     left_on="id",
                                     right_on="id")
        return (playlist_features)

