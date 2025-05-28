from effector_board import EffectorBoard
from .effector import EffectorGui
import flet as ft


class EffectorBoardGui(ft.UserControl):
    def __init__(self, effectorGuis: list[EffectorGui]) -> None:
        super().__init__()

        self.effector_guis = effectorGuis
        self.effector_board: EffectorBoard = EffectorBoard(
            [e.get_effector() for e in effectorGuis]
        )

    def build(self):
        return ft.Row([ft.Card(e) for e in self.effector_guis])
