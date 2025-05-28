import flet as ft


class PlayButton(ft.FilledTonalButton):
    PLAY_TEXT = "再生"
    PAUSE_TEXT = "一時停止"

    def __init__(self, on_click=None):
        self.external_on_click = on_click

        super().__init__(
            text="再生", icon=ft.icons.PLAY_ARROW, on_click=self.button_clicked
        )

    def button_clicked(self, e):
        if self.external_on_click:
            self.external_on_click()

        if self.icon == ft.icons.PLAY_ARROW:
            self.icon = ft.icons.PAUSE
            self.text = PlayButton.PAUSE_TEXT
        else:
            self.icon = ft.icons.PLAY_ARROW
            self.text = PlayButton.PLAY_TEXT

        self.update()
