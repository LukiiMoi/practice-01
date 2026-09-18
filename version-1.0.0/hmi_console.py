"""
HMI en consola para el Simulador de Reactor Químico v1.0.0
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sensors.temperature_sensor import TemperatureSensor
from sensors.pressure_sensor import PressureSensor
from actuators.actuators import CoolingPump, ReliefValve
from modes.automatic_mode import AutomaticMode
from modes.manual_mode import ManualMode
from modes.test_mode import TestMode


class ReactorHMI:
    def __init__(self):
        self.temp = TemperatureSensor()
        self.pressure = PressureSensor()
        self.pump = CoolingPump()
        self.valve = ReliefValve()

        self.auto_mode = AutomaticMode(self.temp, self.pressure, self.pump, self.valve)
        self.manual_mode = ManualMode(self.pump, self.valve)
        self.test_mode = TestMode(self.temp, self.pressure, self.pump, self.valve)

        self.current_mode = "MANUAL"
        self.running = True
        self.last_event = ["Sistema iniciado. Esperando comandos..."]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print("=" * 60)
        print("   SIMULADOR DE REACTOR QUIMICO - HMI v1.0.0")
        print("=" * 60)
        print(f"   MODO ACTUAL: {self.current_mode}")
        print("=" * 60)

    def print_status(self):
        print("\n--- ESTADO ACTUAL DEL SISTEMA ---")
        print(f"   Temperatura : {self.temp.read():>6.1f} C")
        print(f"   Presion     : {self.pressure.read():>6.1f} Bar")
        estado_bomba = "[ACTIVA]" if self.pump.get() > 0 else "[APAGADA]"
        print(f"   Bomba       : {self.pump.get():>3d} %   {estado_bomba}")
        print(f"   Valvula     : {'ABIERTA' if self.valve.is_open() else 'CERRADA'}")
        if self.auto_mode.safety_active:
            print("\n   *** ALERTA: INTERLOCK DE SEGURIDAD ACTIVO ***")

    def print_last_message(self):
        print("\n--- ULTIMA ACCION ---")
        for line in self.last_event:
            print(f"   >> {line}")

    def print_commands(self):
        print("\n" + "-" * 60)
        print("COMANDOS:")
        print("   m             -> cambiar modo (Manual/Auto/Test)")
        print("   s             -> paso de tiempo (solo AUTO)")
        print("   p <0-100>     -> ajustar bomba (solo MANUAL)   ej: p 50")
        print("   v <0|1>       -> valvula abrir/cerrar (MANUAL) ej: v 1")
        print("   f             -> inyectar fallo (solo TEST)")
        print("   r             -> leer sensores")
        print("   q             -> salir")
        print("-" * 60)

    def run(self):
        while self.running:
            self.clear_screen()
            self.print_header()
            self.print_status()
            self.print_last_message()
            self.print_commands()
            cmd = input("\n> ").strip().lower()
            self.process_command(cmd)

    def set_event(self, *lines):
        self.last_event = list(lines)

    # ---------------- PROCESAMIENTO DE COMANDOS ----------------

    def process_command(self, cmd):
        # -------- SALIR --------
        if cmd == 'q':
            self.running = False
            return

        # -------- CAMBIO DE MODO --------
        if cmd == 'm':
            self.clear_screen()
            print("=" * 60)
            print("   SELECCION DE MODO")
            print("=" * 60)
            print("   1. MANUAL")
            print("   2. AUTOMATICO")
            print("   3. PRUEBAS")
            print("-" * 60)
            choice = input("Opcion (1-3): ").strip()
            nombres = {'1': 'MANUAL', '2': 'AUTO', '3': 'TEST'}
            if choice in nombres:
                self.current_mode = nombres[choice]
                self.set_event(f"Modo cambiado a: {self.current_mode}")
            else:
                self.set_event("Opcion invalida. Modo no cambiado.")
            return

        # -------- PASO DE TIEMPO (AUTO) --------
        if cmd == 's':
            if self.current_mode != "AUTO":
                self.set_event(
                    f"El comando 's' solo funciona en modo AUTO.",
                    f"Modo actual: {self.current_mode}. Presiona 'm' y elige 2."
                )
                return

            t_antes = self.temp.read()
            p_antes = self.pressure.read()
            bomba_antes = self.pump.get()

            self.auto_mode.update()

            t_desp = self.temp.read()
            p_desp = self.pressure.read()
            delta_real = t_desp - t_antes
            delta_teorico = 1.5 - (0.05 * bomba_antes)

            lineas = [
                f"[PASO DE TIEMPO] Bomba al {bomba_antes}%",
                f"Formula: DeltaT = 1.5 - (0.05 x {bomba_antes}) = {delta_teorico:+.2f} C",
                f"Temperatura: {t_antes:.1f} -> {t_desp:.1f} C  (delta real {delta_real:+.2f})",
                f"Presion:     {p_antes:.2f} -> {p_desp:.2f} Bar",
            ]

            if self.auto_mode.safety_active:
                lineas.append("*** INTERLOCK ACTIVO: Bomba 100%, Valvula ABIERTA ***")

            self.set_event(*lineas)
            return

        # -------- AJUSTAR BOMBA (MANUAL) --------
        if cmd.startswith('p '):
            if self.current_mode != "MANUAL":
                self.set_event(
                    f"El comando 'p' solo funciona en modo MANUAL.",
                    f"Modo actual: {self.current_mode}. Presiona 'm' y elige 1."
                )
                return
            try:
                valor = int(cmd.split()[1])
                if 0 <= valor <= 100:
                    antes = self.pump.get()
                    self.manual_mode.set_pump(valor)
                    self.set_event(
                        f"BOMBA ajustada: {antes}% -> {self.pump.get()}%",
                        f"Estado bomba: {'ACTIVA' if self.pump.get() > 0 else 'APAGADA'}",
                    )
                else:
                    self.set_event(f"Error: valor fuera de rango (0-100). Recibido: {valor}")
            except (ValueError, IndexError):
                self.set_event("Error: comando invalido. Usa: p 50")
            return

        # -------- VALVULA (MANUAL) --------
        if cmd.startswith('v '):
            if self.current_mode != "MANUAL":
                self.set_event(
                    f"El comando 'v' solo funciona en modo MANUAL.",
                    f"Modo actual: {self.current_mode}. Presiona 'm' y elige 1."
                )
                return
            try:
                valor = int(cmd.split()[1])
                if valor == 1:
                    self.manual_mode.set_valve(1)
                    self.set_event("VALVULA: CERRADA -> ABIERTA")
                elif valor == 0:
                    self.manual_mode.set_valve(0)
                    self.set_event("VALVULA: ABIERTA -> CERRADA")
                else:
                    self.set_event("Error: usa v 1 (abrir) o v 0 (cerrar)")
            except (ValueError, IndexError):
                self.set_event("Error: comando invalido. Usa: v 1 o v 0")
            return

        # -------- INYECTAR FALLO (TEST) --------
        if cmd == 'f':
            if self.current_mode != "TEST":
                self.set_event(
                    f"El comando 'f' solo funciona en modo TEST.",
                    f"Modo actual: {self.current_mode}. Presiona 'm' y elige 3."
                )
                return

            self.clear_screen()
            print("=" * 60)
            print("   INYECCION DE FALLOS")
            print("=" * 60)
            print("   1. TEMPERATURA_ALTA   (forzar 95 C)")
            print("   2. PRESION_ALTA       (forzar 13.5 Bar)")
            print("   3. SENSOR_OFFSET      (offset aleatorio)")
            print("   4. ACTUADOR_SATURADO  (bomba 100% + valvula abierta)")
            print("   5. RUIDO_ALEATORIO    (ruido en presion)")
            print("   6. LIMPIAR            (restaurar valores)")
            print("-" * 60)
            choice = input("Opcion (1-6): ").strip()

            mapping = {
                '1': "TEMPERATURA_ALTA",
                '2': "PRESION_ALTA",
                '3': "SENSOR_OFFSET",
                '4': "ACTUADOR_SATURADO",
                '5': "RUIDO_ALEATORIO",
            }

            if choice == '6':
                self.test_mode.clear_fault()
                self.set_event(
                    "Fallos limpiados. Sistema restaurado.",
                    f"Temp: {self.temp.read():.1f} C  |  Presion: {self.pressure.read():.2f} Bar"
                )
            elif choice in mapping:
                self.test_mode.inject_fault(mapping[choice])
                self.set_event(
                    f"Fallo inyectado: {mapping[choice]}",
                    f"Temp: {self.temp.read():.1f} C  |  Presion: {self.pressure.read():.2f} Bar",
                )
            else:
                self.set_event("Opcion invalida. No se inyecto ningun fallo.")
            return

        # -------- LEER SENSORES --------
        if cmd == 'r':
            self.set_event(
                f"Lectura -> Temp: {self.temp.read():.1f} C  |  Presion: {self.pressure.read():.2f} Bar",
                f"Bomba: {self.pump.get()}%  |  Valvula: {'ABIERTA' if self.valve.is_open() else 'CERRADA'}",
            )
            return

        # -------- COMANDO VACIO --------
        if cmd == '':
            self.set_event("Presiona un comando. Escribe 'm' para cambiar modo.")
            return

        # -------- COMANDO DESCONOCIDO --------
        self.set_event(
            f"Comando no reconocido: '{cmd}'",
            "Comandos validos: m, s, p <val>, v <0|1>, f, r, q"
        )


if __name__ == "__main__":
    ReactorHMI().run()