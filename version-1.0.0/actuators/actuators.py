"""
Actuadores del reactor: Bomba de Enfriamiento y Válvula de Alivio.
"""


class Actuator:
    def __init__(self, name, min_value, max_value):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = min_value

    def set(self, value):
        if self.min_value <= value <= self.max_value:
            self.current_value = value
        else:
            raise ValueError(
                f"[{self.name}] Valor fuera de rango: {value} "
                f"(rango válido: {self.min_value} - {self.max_value})"
            )

    def get(self):
        return self.current_value


class CoolingPump(Actuator):
    """Bomba de enfriamiento con modulación proporcional (0 - 100%)."""

    def __init__(self):
        super().__init__("Bomba de Enfriamiento", 0, 100)

    def set_percentage(self, percentage):
        self.set(int(percentage))


class ReliefValve(Actuator):
    """Válvula de alivio digital ON/OFF (0 = cerrada, 1 = abierta)."""

    def __init__(self):
        super().__init__("Válvula de Alivio", 0, 1)

    def open(self):
        self.set(1)

    def close(self):
        self.set(0)

    def is_open(self):
        return self.current_value == 1