/*
 * Definiciones de comandos seriales para el Micro-Invernadero ESP32.
 * Este archivo es solo documental para mantener la organizacion del proyecto.
 */

#ifndef COMMANDS_H
#define COMMANDS_H

// Comandos disponibles via Monitor Serie
// (El procesamiento real esta en esp32_invernadero.ino)

#define CMD_LEER    "leer"     // Telemetria completa en JSON
#define CMD_TEMP    "temp"     // Temperatura actual
#define CMD_LUZ     "luz"      // Nivel de luz ambiental
#define CMD_FAN     "fan"      // Velocidad del ventilador
#define CMD_LED     "led"      // Intensidad del LED
#define CMD_HELP    "help"     // Ayuda

#endif  // COMMANDS_H