1.  r            → Debe mostrar valores iniciales (25°C, 1.0 Bar)
2.  p 50         → "BOMBA ajustada: 0% -> 50%" + [ACTIVA]
3.  v 1          → "VALVULA: CERRADA -> ABIERTA"
4.  p 0          → "BOMBA ajustada: 50% -> 0%" + [APAGADA]
5.  v 0          → "VALVULA: ABIERTA -> CERRADA"
6.  s            → "El comando 's' solo funciona en modo AUTO"
7.  f            → "El comando 'f' solo funciona en modo TEST"
8.  m  → 2       → "Modo cambiado a: AUTO"
9.  s            → "Temperatura: 25.0 -> 26.5 C (delta real +1.50)"
10. s (x10)      → Temperatura sube progresivamente
11. m  → 3       → "Modo cambiado a: TEST"
12. f  → 1       → Temperatura salta a 95°C
13. m  → 2       → Volver a AUTO
14. s            → Interlock se activa → verás "*** INTERLOCK ACTIVO ***"
15. m  → 3 → f  → 6   → Fallos limpiados
16. q            → Salir


python version-1.0.0/hmi_console.py