import wrapi.py.computing.Normalization as normalization


class RemoteDCMotor(object):
    def __init__(self):
        self._powerMaximum = normalization.maximumValue
        self._powerMinimum = normalization.minimumValue

    @property
    def powerMaximum(self):
        return self._powerMaximum

    @property
    def powerMinimum(self):
        return self._powerMinimum

    # ##Future: Implement this class.
