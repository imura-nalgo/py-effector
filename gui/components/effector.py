import flet as ft
from abc import ABCMeta, abstractmethod
from effectors.effector import Effector


class EffectorGui(ft.UserControl, metaclass=ABCMeta):
    def __init__(self, effctor: Effector) -> None:
        self.title = ft.Text(effctor.name, style=ft.TextThemeStyle.TITLE_MEDIUM)
        super().__init__()

    @abstractmethod
    def get_effector(self) -> Effector:
        raise NotImplementedError()
