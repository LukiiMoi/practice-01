"""
Práctica 2: Script Principal (Bucle Polimórfico)
"""
from nodos import NodoSensor, NodoActuador

def main():
    print("=== INICIANDO SIMULACIÓN DE RED IoT ===\n")

    sensor_temp = NodoSensor("S-01", "192.168.1.10", "Invernadero A", "Temperatura", 30.0)
    actuador_ventilador = NodoActuador("A-01", "192.168.1.20", "Invernadero A", "Ventilador")
    sensor_luz = NodoSensor("S-02", "192.168.1.11", "Invernadero B", "Luminosidad", 50.0)

    red_iot = [sensor_temp, actuador_ventilador, sensor_luz]

    print("--- Conectando dispositivos ---")
    for dispositivo in red_iot:
        print(dispositivo.conectar())


    print("\n--- Simulando cambios en el entorno ---")
    sensor_temp.lectura_actual = 34.5
    actuador_ventilador.encender(100)
    sensor_luz.lectura_actual = 20.0 
    sensor_temp.set_limite_alerta(35.0) 
    
    print("\n--- BUCLE POLIMÓRFICO (Telemetría) ---")
    for dispositivo in red_iot:
        respuesta = dispositivo.enviar_telemetria()
        print(respuesta)

if __name__ == "__main__":
    main()
