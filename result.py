# Libraries
import os
import re
import eyed3
import pytube
import webbrowser
from pathlib import Path
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Connecting with spotify api
load_dotenv()
auth = SpotifyClientCredentials(
    os.getenv("sp_client_id"),
    os.getenv("sp_client_secret"),
)
sp = Spotify(auth_manager=auth)

# Connecting with youtube api
yt = build(
    os.getenv("yt_service_name"),
    os.getenv("yt_api_version"),
    developerKey=os.getenv("yt_developer_key"),
)

# Playlist link
playlist_link = input("Enter Playlist link : ")
# playlist_link = (
#     "https://open.spotify.com/playlist/3ua7cas0riaebaixijDaoq?si=1dedb4f6e6e04ff4"
# )
# playlist_link = (
#     "https://open.spotify.com/playlist/48R8WFVbjl8rO1iFfr9Hxs?si=a27673c96bb14ed1"
# )
playlist_data = sp.playlist(playlist_link)

# Storing data
playlist_name = playlist_data["name"]
print(f"Fetching info from your playlist: {playlist_name}")
total_tracks = playlist_data["tracks"]["total"]
tracks = playlist_data["tracks"]
spotify_items = tracks["items"]

track_artist_list = []
offset = 0
for i in range(total_tracks):
    track_artist_list.append(
        [
            spotify_items[i - offset]["track"]["name"],
            spotify_items[i - offset]["track"]["artists"][0]["name"],
        ]
    )
    if (i + 1) % 100 == 0:
        tracks = sp.next(tracks)
        spotify_items = tracks["items"]
        offset = i + 1

# Delete track data which are removed from spotify
track_artist_list = list(
    filter(
        lambda x: "".join(x).strip() not in [None, ""],
        track_artist_list,
    )
)

total_not_found_tracks = total_tracks - len(track_artist_list)
total_found_tracks = len(track_artist_list)
print(
    f"Playlist Name: {playlist_name} \nTotal Tracks: {total_tracks}\nFound: {total_found_tracks}\nNot Found: {total_not_found_tracks}"
)

# List of queries
query_list = list(map(lambda x: " ".join(x[::-1]), track_artist_list))

# Download path
path_to_download_folder = os.path.join(Path.home(), "Downloads") + "\\" + playlist_name
print(f"Downloading your favorites songs at: {path_to_download_folder}")

track_no = 1
total_failed_tracks = 0
total_downloaded_tracks = 0
# Fetching Links and downloading files
for i, query in enumerate(query_list):
    try:
        # Fetching Links
        # Using Pytube
        s = pytube.Search(query)
        track_id = s.results[0].video_id

        # Using Youtube Data API
        # request = yt.search().list(
        #     part="snippet",
        #     q=query,
        #     maxResults=1,
        #     order="viewCount",
        #     type="video",
        # )
        # response = request.execute()
        # yt_items = response["items"][0]
        # track_id = yt_items["id"]["videoId"]
        link = f"https://www.youtube.com/watch?v={track_id}"

        # Downloading tracks
        link_data = pytube.YouTube(link)
        audio = link_data.streams.filter(only_audio=True).last()
        track_name = " by ".join(track_artist_list[i])
        clean_track_name = re.sub(r'["\/:?<>|]', "", track_name)
        audio.download(path_to_download_folder, f"{clean_track_name}.mp3", timeout=15)
        print(f"{track_no}] Downloaded -> {clean_track_name}")

        # Meta data update
        # track = eyed3.load("song.mp3")
        # track.tag.track_num = track_no
        # track.tag.artist = "Token Entry"
        # track.tag.album = "Free For All Comp LP"
        # track.tag.album_artist = "Various Artists"
        # track.tag.title = "The Edge"

        total_downloaded_tracks += 1
        track_no += 1
    except Exception as error_log:
        total_failed_tracks += 1
        print(f"Failed -> {clean_track_name}")
        print(error_log)

# Open Folder
if total_downloaded_tracks > 0:
    print(
        f"Total Downloaded Tracks: {total_downloaded_tracks}\nTotal Failed Tracks: {total_failed_tracks}"
    )
    print(f"Opening your folder {playlist_name}")
    webbrowser.open(path_to_download_folder)
