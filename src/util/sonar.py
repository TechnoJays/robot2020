from typing import Union

import hal

from wpilib import SendableBase
from wpilib import SendableBuilder
from wpilib import AnalogInput

__all__ = ["MaxSonar"]


class MaxSonar(SendableBase):
    """MaxSonar MB1200

    Designed for MaxSonar using an analog channel
    """
    _vcc: float = None
    _scaling_factor: int = None
    _scaling_ratio: float = None

    def __init__(self, channel: Union[AnalogInput, int], vcc: float = 5.0, scaling_factor: int = 1024) -> None:
        super().__init__()
        if not hasattr(channel, "getAverageVoltage"):  # If 'channel' is an integer
            self.analogChannel = AnalogInput(channel)
            self.allocatedChannel = True
            self.addChild(self.analogChannel)
        else:
            self.allocatedChannel = False
            self.analogChannel = channel
        hal.report(
            hal.tResourceType.kResourceType_AnalogChannel,
            self.analogChannel.getChannel(),
        )
        self.setName("MaxSonar", self.analogChannel.getChannel())
        self._vcc = vcc
        self._scaling_factor = scaling_factor
        self._calculate_scaling()

    def _calculate_scaling(self) -> None:
        self._scaling_ratio = 1.0 * self._scaling_factor / self._vcc

    def close(self) -> None:
        super().close()
        if self.analogChannel and self.allocatedChannel:
            self.analogChannel.close()
        self.analogChannel = None

    def setVcc(self, vcc: float) -> None:
        self._vcc = vcc
        self._calculate_scaling()

    def setScalingFactor(self, factor: int) -> None:
        self._scaling_factor = factor
        self._calculate_scaling()

    def get_distance(self) -> float:
        """Return the distance in centimeters.

        :returns: distance in cm
        """
        if not self.analogChannel:
            return 0.0
        return self.analogChannel.getAverageVoltage() * self._scaling_ratio

    def initSendable(self, builder: SendableBuilder) -> None:
        builder.setSmartDashboardType("AnalogInput")
        builder.addDoubleProperty("Value", self.getDistance, None)
