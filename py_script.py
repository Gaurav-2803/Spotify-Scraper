import flet as ft
import os


def main(page):
    def add_clicked(e):
        pass

    new_task = ft.TextField(hint_text="Playlist Link", width=300)
    page.add(
        ft.Row(
            [
                new_task,
                ft.ElevatedButton(
                    "Download",
                    on_click=add_clicked,
                ),
            ]
        )
    )
    return new_task.value


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
