"""
Práctica 2: Sistema Modular de Nodos IoT
Contiene la superclase NodoIoT y sus subclases (NodoSensor y NodoActuador).
"""

class NodoIoT:
    """Superclase Padre"""
    def __init__(self, id_dispositivo, ip, ubicacion):
        self.id_dispositivo = id_dispositivo
        self.ip = ip
        self.ubicacion = ubicacion
        self.conectado = False
        
    def conectar(self):
        self.conectado = True
        return f"[{self.id_dispositivo}] Conectado a la red en {self.ip}."
        
    def enviar_telemetria(self):
        if not self.conectado:
            return f"[{self.id_dispositivo}] Error: Dispositivo desconectado."
        return f"[{self.id_dispositivo}] Telemetría genérica."

class NodoSensor(NodoIoT):
    """Subclase Hija: Sensor (Herencia y Encapsulamiento)"""
    def __init__(self, id_dispositivo, ip, ubicacion, tipo_sensor, limite_alerta):
        super().__init__(id_dispositivo, ip, ubicacion)
        self.tipo_sensor = tipo_sensor
        self.__limite_alerta = limite_alerta
        self.lectura_actual = 0.0

    def set_limite_alerta(self, nuevo_limite):
        if nuevo_limite < 0:
            print(f"⚠️ Error: El límite de alerta no puede ser negativo.")
            return
        self.__limite_alerta = nuevo_limite
        print(f"[{self.id_dispositivo}] Límite actualizado a {self.__limite_alerta}")

    def enviar_telemetria(self):
        if not self.conectado:
            return f"[{self.id_dispositivo}] Error: Sensor desconectado."
        estado = "⚠️ ALERTA" if self.lectura_actual >= self.__limite_alerta else "Normal"
        return f"📡 [SENSOR] {self.tipo_sensor} ({self.ubicacion}) | Lectura: {self.lectura_actual} | Límite: {self.__limite_alerta} | {estado}"

class NodoActuador(NodoIoT):
    """Subclase Hija: Actuador (Herencia y Encapsulamiento)"""
    def __init__(self, id_dispositivo, ip, ubicacion, tipo_actuador):
        super().__init__(id_dispositivo, ip, ubicacion)
        self.tipo_actuador = tipo_actuador
        self.__estado_activo = False
        self.__potencia_pwm = 0

    def encender(self, potencia=100):
        if not (0 <= potencia <= 100):
            print("⚠️ Potencia inválida. Debe ser 0-100.")
            return
        self.__estado_activo = True
        self.__potencia_pwm = potencia
        print(f"[{self.id_dispositivo}] {self.tipo_actuador} ENCENDIDO al {self.__potencia_pwm}%")

    def apagar(self):
        self.__estado_activo = False
        self.__potencia_pwm = 0
        print(f"[{self.id_dispositivo}] {self.tipo_actuador} APAGADO")

    def enviar_telemetria(self):
        if not self.conectado:
            return f"[{self.id_dispositivo}] Error: Actuador desconectado."
        estado = "ENCENDIDO" if self.__estado_activo else "APAGADO"
        return f"⚙️ [ACTUADOR] {self.tipo_actuador} ({self.ubicacion}) | Estado: {estado} | PWM: {self.__potencia_pwm}%"
