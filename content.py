from flet import *
import download_playlist


def main(page: Page):
    def change_path_status(a):
        folder_path.disabled = folder_path.disabled == False
        page.update()

    def send_info(a):
        link, path = playlist_link.value, folder_path.value
        download_playlist.__start(link, path)

    page.title = "Spotify Scraper"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.bgcolor = "#0B0B0D"
    # page.theme = Theme(color_scheme=ColorScheme(secondary="#D3D5FD"))
    heading = Text(
        value="Spotify Scraper",
        size=60,
        height=90,
        color="#D3D5FD",
    )
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
        hint_text="Folder Path = Downloads",
        width=500,
        bgcolor="#474A56",
        border_width=2,
        border_color="#929AAB",
        color="#D3D5FD",
        disabled=True,
    )
    path_change_chk = Checkbox(
        label="Change Download Location?",
        value=False,
        fill_color="#D3D5FD",
        on_change=change_path_status,
    )
    download_btn = ElevatedButton(
        text="Download",
        height=30,
        width=115,
        on_click=send_info,
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=3)),
    )
    page.add(
        Column(
            [
                heading,
            ],
            height=100,
            alignment=CrossAxisAlignment.CENTER,
        ),
        Column(
            [
                playlist_link,
                folder_path,
            ],
            spacing=15,
            alignment=CrossAxisAlignment.CENTER,
        ),
        Row(
            [
                path_change_chk,
                download_btn,
            ],
            height=40,
            spacing=50,
            alignment=MainAxisAlignment.CENTER,
        ),
    )


app(target=main, view=AppView.WEB_BROWSER, port=45000)
