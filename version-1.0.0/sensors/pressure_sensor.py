"""
Sensor de presión del reactor (0 - 15.0 Bar).
"""
from .base_sensor import AnalogSensor


class PressureSensor(AnalogSensor):
    def __init__(self):
        super().__init__("Presión", 0.0, 15.0, 1.0)