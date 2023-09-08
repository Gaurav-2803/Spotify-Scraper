from flet import *
import os
import re
import pytube
import webbrowser
from pathlib import Path
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from googleapiclient.discovery import build


def spotify_download(link, path):
    pass


def main(page: Page):
    def send_info(a):
        link, path = playlist_link.value, folder_path.value
        spotify_download(link, path)

    page.title = "Spotify Scraper"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.bgcolor = "#0B0B0D"

    playlist_link = TextField(
        hint_text="Playlist Link",
        width=500,
        bgcolor="#474A56",
        border_width=2,
        border_color="#929AAB",
        color="#D3D5FD",
        autofocus=True,
    )
    folder_path = TextField(
        hint_text="Folder Path",
        width=500,
        bgcolor="#474A56",
        border_width=2,
        border_color="#929AAB",
        color="#D3D5FD",
    )
    page.add(
        Column(
            [
                playlist_link,
                folder_path,
            ],
            spacing=20,
            alignment=CrossAxisAlignment.CENTER,
        ),
        Row(
            [
                Checkbox(
                    label="Change Download Location ?",
                    value=False,
                ),
                ElevatedButton(
                    "Download",
                    height=40,
                    width=125,
                    on_click=send_info,
                ),
            ],
            spacing=50,
            alignment=MainAxisAlignment.CENTER,
        ),
    )


app(target=main, view=AppView.WEB_BROWSER, port=45000)
