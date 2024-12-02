import network
import espnow
from machine import ADC, Pin, I2C
import  time 
from ssd1306 import SSD1306_I2C

# OLED Display
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = SSD1306_I2C(128, 64, i2c)

# ESP-NOW initialisieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)

# MAC-Adresse des Auto-ESP32 hinzufügen (Empfänger)
AUTO_MAC = b'\xcc{\\\x98hH'  # MAC-Adresse Auto
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

def on_receive(mac, message):
    command = message.decode('utf-8')
    battery_v, battery_per = map(int, command.split(","))
    battery_v = round(battery_v/1000,2)
    print(f"Empfangen: Batteriespannung {battery_v}, Ladezustand {battery_per}")
    display.fill(0)                         # fill entire screen with colour=0
    display.text(f'{battery_v}V', 0, 0, 1)
    display.text(f'{battery_per}%', 0, 10, 1)
    display.show()
        
try:
    while True:
        command = joystick_to_motor_command()
        esp.send(AUTO_MAC, command.encode('utf-8'))  # Sende die Joystickdaten an das Auto
        #print(f"Gesendeter Befehl: {command}")
        host, msg = esp.recv()
        if msg:
            esp.irq(on_receive(host,msg ))
        else:
            display.fill(0)
            display.text('Hello, World!', 10, 22, 1)
            display.show()
        time.sleep_ms(10)  # Sende alle 10ms
except:
    exit()