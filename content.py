from flet import *
import download_playlist


def main(page: Page):
    def change_path_status(a):
        folder_path.disabled = folder_path.disabled == False
        page.update()

    def send_info(a):
        link, path = playlist_link.value, folder_path.value
        download_playlist.__start(
            page,
            link,
            path,
        )

    page.title = "Spotify Scraper"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.bgcolor = "#0B0B0D"
    heading = Text(
        value="Spotify Scraper",
        style=TextThemeStyle.DISPLAY_LARGE,
        color="#D3D5FD",
    )
    playlist_link = TextField(
        label="Playlist Link",
        hint_text="Playlist Link",
        width=500,
        color="#D3D5FD",
        bgcolor="#474A56",
        border_width=2,
        border_color="#929AAB",
        autofocus=True,
    )
    folder_path = TextField(
        label="Folder Path",
        hint_text="Folder Path = Downloads",
        width=500,
        color="#D3D5FD",
        bgcolor="#474A56",
        border_width=2,
        border_color="#929AAB",
        disabled=True,
        helper_text="Default location is Download folder",
    )
    path_change_chk = Checkbox(
        label="Change Download Location?",
        value=False,
        fill_color="#D3D5FD",
        on_change=change_path_status,
    )
    download_btn = ElevatedButton(
        text="Download",
        on_click=send_info,
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=3)),
    )
    page.add(
        Column(
            [
                heading,
            ],
        ),
        Column(
            [
                playlist_link,
                folder_path,
            ],
            spacing=MainAxisAlignment.SPACE_BETWEEN,
        ),
        Row(
            [
                path_change_chk,
                download_btn,
            ],
            spacing=MainAxisAlignment.SPACE_BETWEEN,
            alignment=MainAxisAlignment.CENTER,
        ),
    )


app(target=main, view=AppView.WEB_BROWSER, port=45000)
