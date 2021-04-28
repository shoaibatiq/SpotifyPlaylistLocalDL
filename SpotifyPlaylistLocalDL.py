#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pytube
from csv import writer, reader
from youtubesearchpython import VideosSearch
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

def append_list_as_row(file_name, list_of_elem):
    """Append downloaded song to csv"""
    with open(file_name, 'a+', newline='', encoding='cp1252') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)
        
def csv_read_rows(filename):
    """Read CSV"""
    rows=[]
    with open(filename, 'r', encoding='cp1252') as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            rows.append(row)
    return rows
def get_downloaded_songs():
    """Get list of already downloaded songs from downloaded_song.csv"""
    return [i[0] for i in csv_read_rows('downloaded_song.csv')]

def get_playlist_from_sp(playlist_user_id, playlist_id, sp_client_id, sp_client_secret):
    """
Get list of all tracks using spotify developer api.

playlist_user_id : user id of playlist owner.
playlist_id : id for playlist to be downloaded.
sp_client_id : client id from spotify developer dashboard.
sp_client_secret : client secret id from spotify developer dashboard.
    """
    auth_manager = SpotifyClientCredentials(
        sp_client_id, 
        sp_client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist = sp.user_playlist_tracks(playlist_user_id, playlist_id)


    playlist = playlist['items']
    return playlist

def get_songs_names(playlist):
    """Get names of songs in playlist to search on YT."""
    songs = []
    for song in playlist:
        song = song['track']
        name = ''
        for artist in song['artists']:
            name += artist['name'] + ', '
        name = name[:-2]
        name += ' - ' + song['name']
        songs.append(name)
    return songs
def download_all_songs(songs):
    """Download all songs from given list and store in songs folder in working dir.
    songs: list of names of songs to download from YT.
    """
    yt_watch="https://www.youtube.com/watch/{}"
    for song in songs:
        print(f'[downloading] {song}')
        videosSearch = VideosSearch(song, limit = 2)


        vid_id = videosSearch.result()['result'][0]['id']

        yt_vid=yt_watch.format(vid_id)

        youtube = pytube.YouTube(yt_vid)

        streams = youtube.streams

        audio = streams.filter(only_audio=True).first()

        out_file = audio.download('songs')
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        append_list_as_row('downloaded_song.csv', [song])
   


# In[4]:


if __name__ == "__main__":
    
    try:
        downloaded_song = get_downloaded_songs() #get listof already downloaded songs
    except:
        downloaded_song = []

    playlist = get_playlist_from_sp(
        'playlist_user_id', 'playlist_id', 
        'sp_client_id', 'sp_client_secret'
    ) #get playlist tracks
    songs = get_songs_names(playlist) #get songs names
    songs = list(filter(lambda x : x not in downloaded_song, songs)) #elimnate already downloaded songs
    download_all_songs(songs) #download all songs


# In[ ]:





# In[27]:




