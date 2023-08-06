from flet import *


def main(page: Page):
    def show_link(a):
        link = new_task.value
        return link

    page.title = "Spotify Scraper"
    new_task = TextField(hint_text="Playlist Link", width=500)
    page.add(
        Row(
            [
                new_task,
                ElevatedButton("Download", on_click=show_link),
            ],
            alignment=MainAxisAlignment.CENTER,
        )
    )


app(target=main, view=AppView.WEB_BROWSER, port=45000)
