import numpy as np
from effectors.effector import Effector

class EffectorBoard:
    def __init__(self, effectors: list[Effector]) -> None:
        self.effectors = effectors

    def print_effector_chain(self) -> None:
        print(" -> ".join([e.get_name() for e in self.effectors]))
    
    def effect(self, input: np.ndarray) -> np.ndarray:
        output = input
        for effector in self.effectors:
            output = effector.effect(output)

        return output