from effectors.effector import Effector
import numpy as np

from parameters.distortion_parameters import DistortionParameters

class Distortion(Effector):
    def __init__(self) -> None:
        self.name = "Distortion"
        self.drive = 10
    
    def distort(self, x: np.int16) -> np.int16:
        """
        1フレームの音声信号に対してひずみを加える

        引数:
            x: np.int16
                入力値
        
        戻り値:
            y: np.int16
                出力値
        """
        x = x * self.drive

        if x > 32767:
            return 32767
        if x < -32768:
            return -32768

        return x

    def set_parameters(self, parameters: DistortionParameters):
        self.drive = parameters.drive
    
    def effect(self, input: np.ndarray) -> np.ndarray:
        return np.array([self.distort(x) for x in input]).astype(np.int16)