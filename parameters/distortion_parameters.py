from exceptions import NotRequiredParamtersSetException
from parameters.parameters import Parameters

class DistortionParameters(Parameters):
    def __init__(self, drive):
        if drive is None:
            raise NotRequiredParamtersSetException()

        self.drive = drive