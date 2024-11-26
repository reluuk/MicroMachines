import network
import espnow
from machine import Pin, PWM
import time

# ESP-NOW initialisieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)

# Auto-Motor-Setup (H-Brücke)
motor_in1 = Pin(27, Pin.OUT)
motor_in2 = Pin(26, Pin.OUT)
motor_pwm = PWM(Pin(25), freq=1000)

# Servo-Setup für die Lenkung
servo_pin = PWM(Pin(15), freq=50)  # 50 Hz für Servo

# Funktion zur Lenkung
def steer_car(x_cmd):
    min_joystick = -100
    max_joystick = 100
    min_servo = 52
    max_servo = 100
    # Mappe den Bereich von -100 bis 100 auf Servo-Winkel (ca. 40 bis 140)
    joystick_value = max(min_joystick, min(max_joystick, x_cmd))
    
    # Perform the scaling
    position = int(min_servo + (joystick_value - min_joystick) / (max_joystick - min_joystick) * (max_servo - min_servo))
    
    #position = int((40 + x_cmd )* 0.9)
    print(position)
    servo_pin.duty(position)

# Funktion zum Fahren
def drive_car(y_cmd):
    if y_cmd > 0:
        motor_in1.on()
        motor_in2.off()
    elif y_cmd < 0:
        motor_in1.off()
        motor_in2.on()
    else:
        motor_in1.off()
        motor_in2.off()
    
    # PWM zur Geschwindigkeitsregelung
    motor_pwm.duty(abs(y_cmd) * 10)

# Callback für empfangene ESP-NOW-Nachrichten
def on_receive(mac, message):
    command = message.decode('utf-8')
    x_cmd, y_cmd = map(int, command.split(","))
    print(f"Empfangener Befehl: Lenkung {x_cmd}, Geschwindigkeit {y_cmd}")
    
    # Steuere das Auto basierend auf den empfangenen Daten
    steer_car(x_cmd)
    if y_cmd > -10 and y_cmd < 10:
        y_cmd = 0
    #drive_car(y_cmd)

print("Auto ist bereit, Befehle zu empfangen.")

# Endlos-Schleife (das Auto wartet auf Nachrichten über den Callback)
while True:
    time.sleep_ms(50)  # Ruhemodus, das Empfangen läuft über den Callback
    # Konfiguriere den Empfang von Nachrichten
    host, msg = esp.recv()
    esp.irq(on_receive(host,msg ))
