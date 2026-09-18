"""
Sensor de temperatura del reactor (0 - 150.0 °C).
"""
from .base_sensor import AnalogSensor


class TemperatureSensor(AnalogSensor):
    def __init__(self):
        super().__init__("Temperatura", 0.0, 150.0, 25.0)

    def to_celsius(self):
        return self.current_value