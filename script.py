""" 
Bugs/Issues: 
    UI: 
        1. Logs showing after completing whole process
Todo:
    UI:
        1. Add Dialog Boxes
        2. New Logs 
    Backend:
        1. Add Meta Data in file such as Cover art, lyrics, artist, etc
        2. Download files from directly browser
        3. Exception handling for user_urls 

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
class scrape_spotify:
    # Load Secrets
    load_dotenv()

    output_logs = Column(controls=[])

    def __init__(self, page, url: str, path: str = ""):
        self.page = page
        self.url = url
        self.download_path = path if path != "" else ""

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

    # Link Type
    def find_entity_type(self):
        self.entity_type = re.search(
            r"^https:\/\/open\.spotify\.com\/(playlist|album|track)\/.*$", self.url
        )[1]

    # Playlist Data
    def __extract_playlist_data(self):
        self.entity_data = scrape_spotify.__sp_obj.playlist(self.url)
        self.tracks = self.entity_data["tracks"]

    # Album Data
    def __extract_album_data(self):
        self.entity_data = scrape_spotify.__sp_obj.album(self.url)
        self.tracks = scrape_spotify.__sp_obj.album_tracks(self.url)

    # Track Data
    def __extract_track_data(self):
        self.spotify_items = (
            self.entity_data
        ) = self.tracks = scrape_spotify.__sp_obj.track(self.url)
        self.entity_name = self.entity_data["name"]
        self.output_logs.controls.append(
            Text(
                value=f"Fetching info from favorite {self.entity_type}:{self.entity_name}"
            )
        )
        self.total_tracks = 1

    # Tracks data in respective entity
    def extract_data(self):
        if self.entity_type == "playlist":
            self.__extract_playlist_data()
        elif self.entity_type == "album":
            self.__extract_album_data()
        elif self.entity_type == "track":
            self.__extract_track_data()
            return
        self.entity_name = self.entity_data["name"]
        self.spotify_items = self.tracks["items"]
        self.output_logs.controls.append(
            Text(
                value=f"Fetching info from favorite {self.entity_type}:{self.entity_name}"
            )
        )
        self.total_tracks = self.entity_data["tracks"]["total"]

    # Make list of Track Name and Artist from Track/Album
    def __track_album_song_artist_data(self):
        if self.entity_type == "track":
            self.spotify_items = [self.spotify_items]
        for track in self.spotify_items:
            self.track_artist_list.append(
                [
                    track["name"],
                    ", ".join(artist_name["name"] for artist_name in track["artists"]),
                ]
            )

    # Make list of Track and Artist from Playlist
    def __playlist_song_artist_data(self):
        offset = 0
        for i in range(self.total_tracks):
            self.track_artist_list.append(
                [
                    self.spotify_items[i - offset]["track"]["name"],
                    ", ".join(
                        artist_name["name"]
                        for artist_name in self.spotify_items[i - offset]["track"][
                            "artists"
                        ]
                    ),
                ]
            )
            if (i + 1) % 100 == 0:
                self.tracks = scrape_spotify.__sp_obj.next(self.tracks)
                self.spotify_items = self.tracks["items"]
                offset = i + 1

    # Make list of Track and Artist
    def song_artist_data(self):
        self.track_artist_list = []
        if self.entity_type in {"album", "track"}:
            self.__track_album_song_artist_data()
        elif self.entity_type == "playlist":
            self.__playlist_song_artist_data()

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
                f"{self.entity_type.capitalize()} Name: {self.entity_name} \nTotal Tracks: {self.total_tracks}\nFound: {self.total_found_tracks}\nNot Found: {self.total_not_found_tracks}"
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
                os.path.join(Path.home(), "Downloads") + "\\" + self.entity_name
                if self.download_path == ""
                else "\\" + self.entity_name
            )
        elif current_os == "Darwin":
            pass
        elif current_os == "Linux":
            self.download_path += (
                os.path.join(Path.home(), "Downloads") + "/" + self.entity_name
                if self.download_path == ""
                else "/" + self.entity_name
            )
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
            request = scrape_spotify.__yt_obj.search().list(
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
        self.total_downloaded_tracks = 0
        self.total_failed_tracks = 0
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
            Text(f"Opening your folder {self.entity_name}")
        )
        self.page.add(self.output_logs)
        self.page.update()
        webbrowser.open(self.download_path)


# https://open.spotify.com/playlist/5PGWUyfX68E4Mzzmxm59rG?si=05889ad869bb4ead
# https://open.spotify.com/album/01GR4NL5O5CZM51k0aejKD?si=WJf2YbQ0QWmYyV3Gysx7Mw
# https://open.spotify.com/track/0g8Dq6OpSmWengqtLrVr77?si=6a06945a467a43fb
def __start(
    page,
    link,
    path="",
):
    ss = scrape_spotify(page, link, path)
    ss.spotify_auth()
    ss.youtube_auth()
    ss.find_entity_type()
    ss.extract_data()
    ss.song_artist_data()
    ss.search_queries()
    ss.set_path()
    ss.search_queries()
    ss.start_download()
    ss.open_folder()
