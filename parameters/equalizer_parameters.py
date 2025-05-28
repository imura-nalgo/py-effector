from exceptions import NotRequiredParamtersSetException
from parameters.parameters import Parameters


class EqualizerParameters(Parameters):
    def __init__(self, hz: int, gain: float):
        if hz is None or gain is None:
            raise NotRequiredParamtersSetException()

        self.hz = hz
        self.gain = gain
