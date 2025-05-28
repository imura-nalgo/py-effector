import flet as ft

from effectors.equalizer import Equalizer
from .effector import EffectorGui
from parameters.equalizer_parameters import EqualizerParameters
from functools import partial


class EqualizerGui(EffectorGui):
    sliders: list[ft.Slider] = []
    GAIN_MAX: int = 10
    GAIN_MIN: int = -25
    DEFAULT_GAIN: int = 0

    def __init__(self) -> None:
        self.equalizer = Equalizer()
        super().__init__(self.equalizer)

        for hz in self.equalizer.bands_hz:
            self.equalizer.set_parameters(
                EqualizerParameters(hz=hz, gain=self.DEFAULT_GAIN)
            )

        self._generate_slides()

    def get_effector(self) -> Equalizer:
        return self.equalizer

    def _generate_slides(self):
        n = 3
        grouped_bands = [
            self.equalizer.bands_hz[i : i + n]
            for i in range(0, len(self.equalizer.bands_hz), n)
        ]

        self.sliders = [
            ft.Container(
                ft.Row(
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Container(
                                        ft.Row(
                                            [
                                                ft.Text(f"""{hz}Hz"""),
                                                ft.Slider(
                                                    min=self.GAIN_MIN,
                                                    max=self.GAIN_MAX,
                                                    divisions=24,
                                                    label="{value}dB",
                                                    value=0,
                                                    expand=True,
                                                    on_change=partial(
                                                        self.on_change_gain_slider,
                                                        band_hz=hz,
                                                    ),
                                                ),
                                            ]
                                        )
                                    )
                                    for hz in g
                                ],
                            )
                        )
                        for g in grouped_bands
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                )
            )
        ]

    def build(self):
        return ft.Container(
            ft.Column(
                [ft.Row([self.title]), *self.sliders],
                spacing=0,
            ),
            padding=15,
        )

    def on_change_gain_slider(self, e: ft.ControlEvent, band_hz: int):
        self.equalizer.set_parameters(
            EqualizerParameters(hz=band_hz, gain=e.control.value)
        )
