import flet as ft

from effectors.distortion import Distortion
from parameters.distortion_parameters import DistortionParameters
from .effector import EffectorGui


class DistortionGui(EffectorGui):
    def __init__(self) -> None:
        self.distortion = Distortion()
        super().__init__(self.distortion)
        self.distortion.set_parameters(DistortionParameters(8))

    def get_effector(self) -> Distortion:
        return self.distortion

    def build(self):
        self.drive_slider = ft.Slider(
            min=1,
            max=100,
            divisions=50,
            label="{value}",
            value=self.distortion.drive,
            on_change=self.on_change_drive_slider,
            expand=True,
        )

        return ft.Container(
            ft.Column(
                [
                    ft.Row([self.title]),
                    ft.Container(
                        ft.Row([ft.Text("Drive"), self.drive_slider]),
                        margin=ft.margin.only(left=15),
                    ),
                ],
                spacing=0,
            ),
            padding=15,
        )

    def on_change_drive_slider(self, e):
        self.distortion.set_parameters(DistortionParameters(self.drive_slider.value))
