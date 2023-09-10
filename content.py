from flet import *
import download_playlist


def main(page: Page):
    def change_path_status(a):
        folder_path.visible = path_change_chk.value != False
        # output.controls.append(Text("Hello"))
        page.update()

    def send_info(a):
        link, path = playlist_link.value, folder_path.value
        download_playlist.__start(
            page,
            link,
            path,
        )

    heading = Text(
        value="Spotify Scraper",
        style=TextThemeStyle.DISPLAY_MEDIUM,
        color="#D3D5FD",
        weight="w800",
    )
    playlist_link = TextField(
        hint_text="Playlist Link",
        autofocus=True,
        color="#D3D5FD",
        bgcolor="#474A56",
        border_width=2,
        border_color="#929AAB",
    )
    folder_path = TextField(
        hint_text="Folder Path = Downloads",
        visible=False,
        color="#D3D5FD",
        bgcolor="#474A56",
        border_width=2,
        border_color="#929AAB",
    )
    path_change_chk = Checkbox(
        label="Change Download Location?",
        value=False,
        fill_color="#D3D5FD",
        on_change=change_path_status,
    )
    download_btn = ElevatedButton(
        text="Download",
        icon="download",
        on_click=send_info,
        style=ButtonStyle(shape=RoundedRectangleBorder(radius=2)),
    )
    output = Column(
        controls=[
            Text(
                value="Logs",
                style=TextThemeStyle.TITLE_LARGE,
                color="#D3D5FD",
                weight="w800",
            ),
            Divider(height=10, color="transparent"),
        ],
    )
    content = Column(
        width=600,
        controls=[
            Row(
                controls=[
                    heading,
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            Divider(height=25, color="transparent"),
            Column(
                controls=[
                    playlist_link,
                    folder_path,
                ],
            ),
            Divider(height=5, color="transparent"),
            Row(
                controls=[
                    path_change_chk,
                    download_btn,
                ],
                alignment=MainAxisAlignment.SPACE_EVENLY,
            ),
            Divider(height=5, color="white"),
            output,
        ],
    )
    page.bgcolor = "#0B0B0D"
    page.title = "Spotify Scraper"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.add(content)
    page.scroll = "always"


app(target=main, view=AppView.WEB_BROWSER, port=45000)
