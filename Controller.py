import network
import espnow
from machine import ADC, Pin
from time import sleep

# ESP-NOW initialisieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)

# MAC-Adresse des Auto-ESP32 hinzufügen (Empfänger)
AUTO_MAC = b'\xcc{\\\x98hH'  # Ersetze XX mit der tatsächlichen MAC-Adresse
esp.add_peer(AUTO_MAC)

# Joystick-Pins initialisieren
x_joystick = ADC(Pin(32))  # Links/Rechts Lenkung
x_joystick.atten(ADC.ATTN_11DB)

y_joystick = ADC(Pin(33))  # Vorwärts/Rückwärts Geschwindigkeit
y_joystick.atten(ADC.ATTN_11DB)

def joystick_to_motor_command():
    # Lese Joystickwerte und mappe auf Bereich -100 bis +100
    x_val = x_joystick.read()
    y_val = y_joystick.read()
    x_cmd = int((x_val - 2048) / 20.48)
    y_cmd = int((y_val - 2048) / 20.48)
    
    # Kommaseparierter String für x und y Befehle
    return f"{x_cmd},{y_cmd}"

while True:
    command = joystick_to_motor_command()
    esp.send(AUTO_MAC, command.encode('utf-8'))  # Sende die Joystickdaten an das Auto
    print(f"Gesendeter Befehl: {command}")
    sleep(0.1)  # Sende alle 100 ms