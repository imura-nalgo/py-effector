from abc import ABCMeta, abstractmethod
import numpy as np

from parameters.parameters import Parameters

class Effector(metaclass=ABCMeta):
    def get_name(self):
        return self.name

    @abstractmethod
    def set_parameters(self, parameters: Parameters):
        """
        パラメータを設定する

        引数:
            parameters: Parameters
                パラメータ
        """
        pass

    @abstractmethod
    def effect(self, input: np.ndarray) -> np.ndarray:
        """
        入力の音声信号に対して効果を加える

        引数:
            input: np.ndarray
                音声信号
        
        戻り値:
            output: np.ndarray
                加工した音声信号
        """
        raise NotImplementedError()