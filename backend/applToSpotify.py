#!/usr/bin/env python

import json
import os
from requests import Session
import requests
from bs4 import BeautifulSoup
from base64 import b64encode
from urllib.parse import urlencode
from dotenv import load_dotenv


class Spotify:
    def __init__(self, token = None) -> None:
        self.session = Session()
        if token == None:
            token = os.getenv('SPOTIFY_OAUTH')
        if not token:
            raise Exception('Please specify the environment variable SPOTIFY_OAUTH') 
        self.session.headers["Authorization"] =  "Bearer " + token
        
    def request(self, endpoint, payload = None, post = False):
        if payload != None or post == True:
            res = self.session.post('https://api.spotify.com/v1' + endpoint, json=payload)
        else:
            res = self.session.get('https://api.spotify.com/v1' + endpoint)
        if not res.ok:
            print(res.text)
            raise Exception('Error occurred during API request ')
        return res.json()
        
    def create_playlist(self, name, appl_playlist_id, img_url = None, des=None, purge_existing = False):
        '''
        Returns -   spotify playlist_id
                    Creates a new one if no matching playlist is found
        '''
        # Checks if playlist is already exported 
        # We could also query the spotify playlists 
        # instead of having a playlists.json but /shrug
        try:
            with open('playlists.json', 'r+') as fp:
                data = json.load(fp)
                id = next((x['spot'] for x in data if x['appl'] == appl_playlist_id), None)
                if id:
                    print(f'Playlist already exported to spotify - id {appl_playlist_id} found in playlists.json')
                    if purge_existing == True or str.upper(input('Purge existing tracks from playlist? [Y/N]: ')) == 'Y' : self.clear_playlist(id)
                    return id
        except IOError: pass
            
        payload = {
            "name": name,
            "description": des,
            "public": True
        }

        # Create a new playlist
        user_id = self.request('/me')['id']
        playlist_id = self.request(f'/users/{user_id}/playlists', payload = payload)['id']
        if img_url: self.update_playlist_artwork(playlist_id, img_url)
            
        playlists = [
            {
                "appl" : appl_playlist_id,
                "spot" : playlist_id
            }
        ]
        try:
            with open('playlists.json', 'r+') as fp:
                data = json.load(fp)    
                data.append(playlists[0])
                fp.seek(0)
                json.dump(data, fp)
                fp.truncate()

        except FileNotFoundError: 
            with open('playlists.json', 'w+') as fp:
                json.dump(playlists, fp)
                
        return playlist_id    

    def add_to_playlist(self, playlist_id, uris):
        url = f'/playlists/{playlist_id}/tracks?'
        tracks = {
            'uris' : uris
        }
        tracks = urlencode(tracks)
        # print(url + tracks)
        self.request(url + tracks, post=True)
        
    def update_playlist_artwork(self, playlist_id, img_url):
        image = requests.get(img_url)
        enc_img = b64encode(image.content)
        r = self.session.put(f'https://api.spotify.com/v1/playlists/{playlist_id}/images', data = enc_img, headers={'Content-type': image.headers['content-type']})
        if not r.ok:
            print(r.text)
            raise Exception('Unable to update playlist artwork')
        
    def clear_playlist(self, playlist_id):
        """Remove all tracks from a Spotify playlist."""
        # Get the list of tracks in the playlist
        tracks_data = self.request(f'/playlists/{playlist_id}/tracks')['items']

        # If the playlist is empty, return immediately
        if not tracks_data:
            return

        # Create a list of track URIs
        track_uris = [{'uri': track['track']['uri']} for track in tracks_data]

        # Remove the tracks from the playlist in chunks of 100
        for i in range(0, len(track_uris), 100):
            chunk = track_uris[i:i + 100]
            response = self.session.delete(
                f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
                json={'tracks': chunk}
            )
            if not response.ok:
                raise Exception('Unable to clear playlist')
            
        
def get_songs_from_apple(id):
    # pl.9a964a33c1484aec8fdb0cac3e7771ed
    url = 'https://music.apple.com/us/playlist/' + id
    res = requests.get(url)
    if not res.ok:
        raise Exception('Unable to fetch playlist')
    d = BeautifulSoup(res.content.decode('utf-8'), "html.parser").find(id='serialized-server-data').contents
 
    if len(d) < 1:
        raise Exception('Unable to find playlist data')
    data = json.loads(d[0])[0]['data']['sections']
    song_data = next(x['items'] for x in (data) if x['itemKind'] == 'trackLockup')
    
    album_data = data[0]['items'][0]
    
    art = album_data['artwork']['dictionary']
    album = {
        'name' : album_data['title'],
        'artwork_url' : art['url'].format(w = '300', h = '300', f = 'jpeg'),
        'tracks' : []        
    }
    for track in song_data:
        song = {
            'title': track['title'],
            'artist': track['artistName'],           
            'arwork': track['artwork']['dictionary']['url'].format(w = '300', h = '300', f = 'jpeg')
        }
        if song['artist'] == "Olivia Rodrigo":
            print('Song:', song['title'])

        album['tracks'].append(song)
        # print(f'{song["title"]:35} - {", ".join(x for x in song["artists"])}')
    
    return album

def main(id):    
    spotify = Spotify()
    playlist = get_songs_from_apple(id)
    
    uris = []
    spotify_id = spotify.create_playlist(playlist['name'] + ' - Apple Music', appl_playlist_id = id, img_url=playlist['artwork_url'])
    
    for s in playlist['tracks']:
        q = {
            'q': s['title'],
            'artist': ' '.join(x for x in s['artists']),
            'type': 'track',
            'limit': 1
        }
        res = spotify.request('/search?' + urlencode(q))
        song_data = res['tracks']['items'][0]
        
        artist = [x['name'] for x in song_data['artists']]
        title = song_data['name']
        uri = song_data['uri']
        uris.append(uri)
        print(f'{title:30} - {", ".join(x for x in artist):10} - {uri}')

        spotify.add_to_playlist(spotify_id, uri)
        
        # break

        
    
if __name__ == '__main__':
    import sys, os
    if len(sys.argv) <= 1:
        sys.exit()
    id = sys.argv[1]
    # main(id)
    # get_auth_token()
  
