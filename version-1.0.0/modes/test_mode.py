"""
Modo de Pruebas: rutina de inyección de fallos.
"""
import random


class TestMode:
    def __init__(self, temp_sensor, pressure_sensor, pump, valve):
        self.temp = temp_sensor
        self.pressure = pressure_sensor
        self.pump = pump
        self.valve = valve

    def inject_fault(self, fault_type):
        fault_type = fault_type.upper()

        if fault_type == "TEMPERATURA_ALTA":
            self.temp.set_value(95.0)
        elif fault_type == "PRESION_ALTA":
            self.pressure.set_value(13.5)
        elif fault_type == "SENSOR_OFFSET":
            offset = random.uniform(-5, 5)
            self.temp.set_value(max(0.0, min(150.0, self.temp.read() + offset)))
        elif fault_type == "ACTUADOR_SATURADO":
            self.pump.set_percentage(100)
            self.valve.open()
        elif fault_type == "RUIDO_ALEATORIO":
            noise = random.uniform(-2, 2)
            self.pressure.set_value(
                max(0.0, min(15.0, self.pressure.read() + noise))
            )
        else:
            return False
        return True

    def clear_fault(self):
        self.temp.set_value(25.0)
        self.pressure.set_value(1.0)
        self.pump.set_percentage(0)
        self.valve.close()