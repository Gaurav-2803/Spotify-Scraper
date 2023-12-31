""" 
Bugs/Issues : 
    Logic: 
        1. Downloading more than once not updating logs and downloading them x times 
    UI: 
        1. Logs showing after completing whole process

"""
# Libraries
import os
import re
import pytube
import platform
import webbrowser
from pathlib import Path
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flet import *


# import eyed3
# from moviepy.editor import *
class playlist:
    load_dotenv()
    # Api Objects
    __sp_obj = None
    __yt_obj = None

    # PLaylist Info
    playlist_data: dict = None
    playlist_name: str = ""
    tracks: dict = None
    spotify_items: dict = None
    track_artist_list: list[(str, str)] = []

    # Track Info
    total_tracks: int = 0
    total_found_tracks: int = 0
    total_not_found_tracks: int = 0
    total_failed_tracks: int = 0
    total_downloaded_tracks: int = 0

    # Others
    download_path: str = ""
    query_list: list[str] = None
    output_logs = Column(controls=[])

    def __init__(self, page, url: str, path: str = ""):
        self.page = page
        self.playlist_url = url
        if path != "":
            self.download_path = path

    # Connecting with spotify api
    @classmethod
    def spotify_auth(cls):
        auth = SpotifyClientCredentials(
            os.getenv("sp_client_id"),
            os.getenv("sp_client_secret"),
        )
        cls.__sp_obj = Spotify(auth_manager=auth)

    # Connecting with youtube api
    @classmethod
    def youtube_auth(cls):
        cls.__yt_obj = build(
            os.getenv("yt_service_name"),
            os.getenv("yt_api_version"),
            developerKey=os.getenv("yt_developer_key"),
        )

    # Playlist Data
    def extract_playlist_data(self):
        self.playlist_data = playlist.__sp_obj.playlist(self.playlist_url)
        self.playlist_name = self.playlist_data["name"]
        self.output_logs.controls.append(
            Text(
                value=f"Fetching info from your playlist: {self.playlist_name}",
            ),
        )
        self.total_tracks = self.playlist_data["tracks"]["total"]
        self.tracks = self.playlist_data["tracks"]
        self.spotify_items = self.tracks["items"]

    # Make list of Track and Artist
    def song_artist_data(self):
        offset = 0
        for i in range(self.total_tracks):
            self.track_artist_list.append(
                [
                    self.spotify_items[i - offset]["track"]["name"],
                    self.spotify_items[i - offset]["track"]["artists"][0]["name"],
                ]
            )
            if (i + 1) % 100 == 0:
                self.tracks = playlist.__sp_obj.next(self.tracks)
                self.spotify_items = self.tracks["items"]
                offset = i + 1

        # Delete track data which are removed from spotify
        self.track_artist_list = list(
            filter(
                lambda x: "".join(x).strip() not in [None, ""],
                self.track_artist_list,
            )
        )

        self.total_not_found_tracks = self.total_tracks - len(self.track_artist_list)
        self.total_found_tracks = len(self.track_artist_list)
        self.output_logs.controls.append(
            Text(
                f"Playlist Name: {self.playlist_name} \nTotal Tracks: {self.total_tracks}\nFound: {self.total_found_tracks}\nNot Found: {self.total_not_found_tracks}"
            )
        )

    # Queries to be searched
    def search_queries(self):
        self.query_list = list(map(lambda x: " ".join(x[::-1]), self.track_artist_list))

    # Set download path
    def set_path(self):
        current_os = platform.system()
        if current_os == "Windows":
            self.download_path += (
                os.path.join(Path.home(), "Downloads") + "\\" + self.playlist_name
                if self.download_path == ""
                else "\\" + self.playlist_name
            )
        elif current_os == "Darwin":
            pass
        elif current_os == "Linux":
            pass
        elif current_os == "Android":
            pass
        elif current_os == "iOS":
            pass
        else:
            self.output_logs.controls.append(Text("Unsupported operating system."))

    # Fetching Links
    @staticmethod
    def fetch_link(query: str) -> str:
        try:
            # Using Youtube Data API
            request = playlist.__yt_obj.search().list(
                part="snippet",
                q=query,
                maxResults=1,
                order="viewCount",
                type="video",
            )
            response = request.execute()
            yt_items = response["items"][0]
            track_id = yt_items["id"]["videoId"]

        except HttpError as error_log:
            if error_log.status_code != 403:
                raise error_log
            # Using Pytube
            s = pytube.Search(query)
            track_id = s.results[0].video_id

        return f"https://www.youtube.com/watch?v={track_id}"

    # Compress File
    def compress_song(self, file: str):
        pass

    # Apply Metadata
    def fit_metadata(self, file: str):
        pass

    # Download songs
    def start_download(self):
        # Fetching Links and downloading files
        self.output_logs.controls.append(
            Text(f"Downloading your favorites songs at: {self.download_path}")
        )
        for track_no, query in enumerate(self.query_list):
            try:
                # Fetch link
                link = self.fetch_link(query)
                # Downloading tracks
                link_data = pytube.YouTube(link)
                video_file = link_data.streams.filter(only_audio=True).first()
                track_name = " by ".join(self.track_artist_list[track_no])
                clean_track_name = re.sub(r'["\/:?<>|]', "", track_name)
                video_file.download(
                    self.download_path, f"{clean_track_name}.mp3", timeout=15
                )

                self.output_logs.controls.append(
                    Text(
                        f"Downloaded ({self.total_downloaded_tracks+1}/{self.total_found_tracks}) -> {clean_track_name}"
                    )
                )
                self.total_downloaded_tracks += 1

            except Exception as error_log:
                self.total_failed_tracks += 1
                self.output_logs.controls.append(Text(f"Failed -> {clean_track_name}"))
                print(error_log)

    # Open output folder
    def open_folder(self):
        self.output_logs.controls.append(
            Text(
                f"Total Downloaded Tracks: {self.total_downloaded_tracks}\nTotal Failed Tracks: {self.total_failed_tracks}"
            )
        )
        self.output_logs.controls.append(
            Text(f"Opening your folder {self.playlist_name}")
        )
        self.page.add(self.output_logs)
        self.page.update()
        webbrowser.open(self.download_path)


def __start(
    page,
    link,
    path="",
):
    pd = playlist(page, link, path)
    pd.spotify_auth()
    pd.youtube_auth()
    pd.extract_playlist_data()
    pd.song_artist_data()
    pd.search_queries()
    pd.set_path()
    pd.search_queries()
    pd.start_download()
    pd.open_folder()
