"""
Modo Automático con algoritmo de estabilidad dinámico e interlocks.
"""


class AutomaticMode:
    def __init__(self, temp_sensor, pressure_sensor, pump, valve):
        self.temp = temp_sensor
        self.pressure = pressure_sensor
        self.pump = pump
        self.valve = valve
        self.safety_active = False

    def check_safety_interlocks(self):
        """Interlocks de seguridad: prioridad máxima."""
        if self.temp.read() > 85.0 or self.pressure.read() > 12.0:
            self.safety_active = True
            self.pump.set_percentage(100)
            self.valve.open()
            return True
        self.safety_active = False
        return False

    def update(self, operation_time=1.0):
        """Aplica la fórmula: DeltaT = 1.5 - (0.05 * %Bomba)"""
        if self.check_safety_interlocks():
            return

        delta_t = 1.5 - (0.05 * self.pump.get())
        new_temp = self.temp.read() + delta_t
        self.temp.set_value(max(0.0, min(150.0, new_temp)))

        pressure_change = 0.05 * (self.pump.get() / 100.0)
        new_pressure = self.pressure.read() + pressure_change
        self.pressure.set_value(max(0.0, min(15.0, new_pressure)))

        self.check_safety_interlocks()