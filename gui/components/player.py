import flet as ft

from player import Player
from .effector_board import EffectorBoardGui


class PlayerGui(ft.UserControl):
    def did_mount(self):
        self.page.overlay.append(self.file_picker_dialog)
        self.page.window.width = 900
        self.page.update()

    def on_window_close(self):
        self.page.window_destroy()

    def __init__(self, src: str, effector_board_gui: EffectorBoardGui) -> None:
        super().__init__()

        self.src = src
        self.effector_board_gui = effector_board_gui
        self.player = Player(src, on_stop=self.on_player_stop)
        self.player.set_effector_board(self.effector_board_gui.effector_board)
        self.selected_audio_file_path = None
        self.selected_audio_file_name = ft.Text("")

    def build(self):
        self.play_button = ft.IconButton(
            icon=ft.icons.PLAY_ARROW,
            on_click=self.on_click_play_button,
            disabled=True,
        )
        self.stop_button = ft.IconButton(
            icon=ft.icons.STOP,
            on_click=self.on_click_stop_button,
            disabled=False,
        )
        self.effector_board_switch = ft.Switch(
            label="エフェクター",
            value=self.player.is_enable_effector_board(),
            on_change=self.on_change_effector_board_switch,
        )
        self.file_pick_button = ft.ElevatedButton(
            "wavファイル選択",
            icon=ft.icons.FILE_UPLOAD,
            on_click=self.on_click_select_file_button,
        )
        self.file_picker_dialog = ft.FilePicker(on_result=self.on_file_picker_result)

        return ft.Card(
            ft.Container(
                ft.Column(
                    [
                        ft.Container(
                            ft.Row(
                                [
                                    self.file_pick_button,
                                    self.selected_audio_file_name,
                                ]
                            ),
                            margin=ft.margin.only(left=10, top=10),
                        ),
                        ft.Container(
                            ft.Row(
                                [
                                    self.play_button,
                                    self.stop_button,
                                    self.effector_board_switch,
                                ]
                            ),
                            margin=ft.margin.only(left=10, top=10),
                        ),
                        ft.Divider(),
                        self.effector_board_gui,
                    ],
                )
            )
        )

    def on_player_stop(self):
        self.play_button.icon = ft.icons.PLAY_ARROW
        self.stop_button.disabled = True

        self.play_button.update()
        self.stop_button.update()

    def on_click_play_button(self, e):
        if self.play_button.icon == ft.icons.PLAY_ARROW:
            self.player.play()
            self.play_button.icon = ft.icons.PAUSE
            self.stop_button.disabled = False
        else:
            self.player.pause()
            self.play_button.icon = ft.icons.PLAY_ARROW
            self.stop_button.disabled = True

        self.play_button.update()
        self.stop_button.update()

    def on_click_stop_button(self, e):
        self.player.stop()

    def on_change_effector_board_switch(self, e):
        if self.player.is_enable_effector_board():
            self.player.disable_effector_board()
            self.effector_board_switch.value = False
        else:
            self.player.enable_effector_board()
            self.effector_board_switch.value = True

        self.effector_board_switch.update()

    def on_click_select_file_button(self, e):
        self.file_picker_dialog.pick_files(allow_multiple=True)

    def on_file_picker_result(self, e: ft.FilePickerResultEvent):
        self.selected_audio_file_path = e.files[0].path
        self.selected_audio_file_name.value = e.files[0].name
        self.selected_audio_file_name.update()

        self.player = Player(self.selected_audio_file_path, on_stop=self.on_player_stop)
        self.player.set_effector_board(self.effector_board_gui.effector_board)

        self.play_button.disabled = False
        self.stop_button.disabled = True

        self.play_button.update()
        self.stop_button.update()
