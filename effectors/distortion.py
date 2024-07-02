from effectors.effector import Effector
import numpy as np

from parameters.distortion_parameters import DistortionParameters

class Distortion(Effector):
    def __init__(self) -> None:
        self.name = "Distortion"
        self.drive = 10
    
    def set_parameters(self, parameters: DistortionParameters):
        self.drive = parameters.drive
    
    def effect(self, input: np.ndarray) -> np.ndarray:
        """
        ディストーションを実装する

        引数:
            input: np.ndarray
                音声信号

        戻り値:
            output: np.ndarray
                加工した音声信号
        """

        # inputはnp.int16でわたってくる。
        # driveをかけた際にオーバーフローが発生するのを防ぐため、一旦np.int64に変換する。
        output = input.astype(np.int64) * self.drive
        output = np.minimum(32767, output)
        output = np.maximum(-32768, output)

        return output.astype(np.int16)