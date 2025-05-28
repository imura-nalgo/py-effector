from effector_board import EffectorBoard

import flet as ft
from gui.components.player import PlayerGui
from gui.components.effector_board import EffectorBoardGui
from gui.components.distortion import DistortionGui
from gui.components.equalizer import EqualizerGui

FILENAME = "./data/guitar.wav"


def main(page: ft.Page):
    page.title = "Python Effector"

    boardGui = EffectorBoardGui([EqualizerGui()])
    page.add(ft.Column([PlayerGui(FILENAME, boardGui)]))
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
