"""
Clase base para sensores analógicos del reactor.
"""

class AnalogSensor:
    """Representa un sensor analógico con rango de operación."""

    def __init__(self, name, min_value, max_value, current_value=0):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value

    def read(self):
        """Devuelve el valor actual del sensor."""
        return self.current_value

    def set_value(self, value):
        """Establece un valor, validando el rango."""
        if self.min_value <= value <= self.max_value:
            self.current_value = value
        else:
            raise ValueError(
                f"[{self.name}] Valor fuera de rango: {value} "
                f"(rango válido: {self.min_value} - {self.max_value})"
            )

    def __str__(self):
        return f"{self.name}: {self.current_value:.1f}"