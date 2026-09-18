"""
Modo Manual: control directo por consola.
"""


class ManualMode:
    def __init__(self, pump, valve):
        self.pump = pump
        self.valve = valve

    def set_pump(self, percentage):
        self.pump.set_percentage(max(0, min(100, int(percentage))))

    def set_valve(self, state):
        if state in (1, True):
            self.valve.open()
        else:
            self.valve.close()