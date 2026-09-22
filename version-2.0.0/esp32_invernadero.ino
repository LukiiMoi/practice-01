/*
 * Micro-Invernadero Inteligente - ESP32
 * Practica 1 - Version 2.0.0
 * Sistema de control con PWM, ADC y Monitor Serie
 */

#include <Arduino.h>

// ============================================
// PINES (Asignacion estricta del enunciado)
// ============================================
#define PIN_TEMP   34   // Sensor termico LM35/DHT - ADC (12 bits)
#define PIN_LDR    32   // Sensor LDR - ADC (12 bits)
#define PIN_FAN    18   // Ventilador Motor DC - PWM (ledc 5kHz)
#define PIN_LED    19   // LED de potencia - PWM (ledc 5kHz)

// ============================================
// CONFIGURACION PWM
// ============================================
#define PWM_FREQ     5000    // 5 kHz
#define PWM_RES      8       // 8 bits (0-255)
#define CH_FAN       0
#define CH_LED       1

// ============================================
// CONSTANTES DE CONTROL
// ============================================
#define TEMP_UMBRAL  30.0    // °C - activa ventilador al 100%
#define ADC_MAX      4095.0  // Resolucion 12 bits
#define VREF         3.3     // Voltaje de referencia del ADC

// ============================================
// VARIABLES GLOBALES
// ============================================
float temperatura = 0.0;   // °C
float luz = 0.0;           // % (0 = oscuridad, 100 = luz plena)
int fan_duty = 0;          // 0-255
int led_duty = 0;          // 0-255

// ============================================
// SETUP
// ============================================
void setup() {
  Serial.begin(115200);
  delay(500);

  pinMode(PIN_TEMP, INPUT);
  pinMode(PIN_LDR, INPUT);

  // Configurar canales PWM
  ledcSetup(CH_FAN, PWM_FREQ, PWM_RES);
  ledcSetup(CH_LED, PWM_FREQ, PWM_RES);
  ledcAttachPin(PIN_FAN, CH_FAN);
  ledcAttachPin(PIN_LED, CH_LED);

  // Estado inicial: ventilador apagado, LED al 50%
  ledcWrite(CH_FAN, 0);
  ledcWrite(CH_LED, 128);

  Serial.println();
  Serial.println("============================================");
  Serial.println("   MICRO-INVERNADERO INTELIGENTE v2.0");
  Serial.println("============================================");
  Serial.println("Comandos disponibles:");
  Serial.println("  leer    -> telemetria completa (JSON)");
  Serial.println("  temp    -> temperatura actual");
  Serial.println("  luz     -> nivel de luz ambiental");
  Serial.println("  fan     -> velocidad del ventilador");
  Serial.println("  led     -> intensidad del LED");
  Serial.println("  help    -> mostrar esta ayuda");
  Serial.println("============================================");
}

// ============================================
// LOOP PRINCIPAL
// ============================================
void loop() {
  leerSensores();
  controlTemperatura();
  controlLuminosidad();
  procesarComandos();
  delay(500);
}

// ============================================
// LECTURA DE SENSORES
// ============================================
void leerSensores() {
  // --- Temperatura (LM35: 10 mV por °C) ---
  int raw_temp = analogRead(PIN_TEMP);
  float voltaje = (raw_temp / ADC_MAX) * VREF;
  temperatura = voltaje * 100.0;   // 10 mV/°C => x100

  // --- Luz ambiental (LDR en divisor de voltaje) ---
  int raw_ldr = analogRead(PIN_LDR);
  luz = (raw_ldr / ADC_MAX) * 100.0;   // Normalizado a 0-100 %
}

// ============================================
// CONTROL DE TEMPERATURA (ON/OFF)
// ============================================
void controlTemperatura() {
  // Gestion termica: ventilador al 100% si T > 30 °C
  if (temperatura > TEMP_UMBRAL) {
    fan_duty = 255;
  } else {
    fan_duty = 0;
  }
  ledcWrite(CH_FAN, fan_duty);
}

// ============================================
// CONTROL DE LUMINOSIDAD (PROPORCIONAL INVERSO)
// ============================================
void controlLuminosidad() {
  // A menor luz natural, mayor intensidad del LED
  // Mapeo: LDR 0-100% -> LED 255-0
  int target = map((int)luz, 0, 100, 255, 0);
  led_duty = constrain(target, 0, 255);
  ledcWrite(CH_LED, led_duty);
}

// ============================================
// PROCESAMIENTO DE COMANDOS SERIALES
// ============================================
void procesarComandos() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toLowerCase();

    if (cmd == "leer" || cmd == "status") {
      enviarTelemetria();
    }
    else if (cmd == "temp") {
      Serial.print("Temperatura: ");
      Serial.print(temperatura, 1);
      Serial.println(" C");
    }
    else if (cmd == "luz") {
      Serial.print("Luz ambiental: ");
      Serial.print(luz, 1);
      Serial.println(" %");
    }
    else if (cmd == "fan") {
      Serial.print("Ventilador: ");
      Serial.print((fan_duty * 100) / 255);
      Serial.println(" %");
    }
    else if (cmd == "led") {
      Serial.print("LED: ");
      Serial.print((led_duty * 100) / 255);
      Serial.println(" %");
    }
    else if (cmd == "help") {
      Serial.println("Comandos: leer, temp, luz, fan, led, help");
    }
    else if (cmd.length() > 0) {
      Serial.print("Comando no reconocido: ");
      Serial.println(cmd);
    }
  }
}

// ============================================
// TELEMETRIA EN FORMATO JSON
// ============================================
void enviarTelemetria() {
  Serial.println("{");
  Serial.print("  \"temperatura\": ");
  Serial.print(temperatura, 1);
  Serial.println(",");
  Serial.print("  \"luz\": ");
  Serial.print(luz, 1);
  Serial.println(",");
  Serial.print("  \"ventilador\": ");
  Serial.print((fan_duty * 100) / 255);
  Serial.println(",");
  Serial.print("  \"led\": ");
  Serial.print((led_duty * 100) / 255);
  Serial.println();
  Serial.println("}");
}