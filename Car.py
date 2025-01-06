import network
import espnow
import time
from machine import Pin, PWM, ADC, I2C
from I2C_LCD_class import I2cLcd
from measure_Class import Battery_Voltage

# ESP-NOW initialisieren
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
esp = espnow.ESPNow()
esp.active(True)

# MAC-Adresse des Controller-ESP32 hinzufügen (Empfänger)
CONTROLLER_MAC = b'\x10\x06\x1c\xd6J\x1c'  # MAC-Adresse Controller
esp.add_peer(CONTROLLER_MAC)

# Auto-Motor-Setup (H-Brücke)
motor_in1 = Pin(26, Pin.OUT)
motor_in2 = Pin(25, Pin.OUT)
motor_pwm = PWM(Pin(27), freq=2000)

# Konfiguration für den ADC Batteriespannung
adc = ADC(Pin(32))  # ADC an GPIO 34
adc.width(ADC.WIDTH_12BIT)  # 12-bit Auflösung (0-4095)
adc.atten(ADC.ATTN_11DB)  # 11dB Attenuation -> max ~3.6V
battery_val = []

# Servo-Setup für die Lenkung
servo_pin = PWM(Pin(15), freq=50)  # 50 Hz für Servo

# LCD
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
devices = i2c.scan()
if len(devices) == 0:
    print("No i2c device !")
else:
    for device in devices:
        print("I2C addr: " + hex(device))
        lcd = I2cLcd(i2c, device, 2, 16)

counter = 0


# Funktion zur Lenkung
def steer_car(x_cmd):
    min_joystick = -100
    max_joystick = 100
    min_servo = 70
    max_servo = 112
    x_cmd = x_cmd
    if x_cmd < -5 and x_cmd > -11:
        x_cmd = -5

    # Mappe den Bereich von -100 bis 100 auf Servo-Winkel (ca. 40 bis 140)
    joystick_value = max(min_joystick, min(max_joystick, x_cmd))

    # Perform the scaling
    position = int(
        min_servo + (joystick_value - min_joystick) / (max_joystick - min_joystick) * (max_servo - min_servo))

    # position = int((40 + x_cmd )* 0.9)
    # print(position)
    servo_pin.duty(position)


# Funktion zum Fahren
def drive_car(y_cmd):
    if y_cmd < 0:
        motor_in1.on()
        motor_in2.off()
    elif y_cmd > 0:
        motor_in1.off()
        motor_in2.on()
    else:
        motor_in1.off()
        motor_in2.off()

    # PWM zur Geschwindigkeitsregelung
    motor_pwm.duty(abs(y_cmd) * 10)


def average_val(buffer, value, max_size=50):
    # Wert zur Liste hinzufügen und älteste Werte entfernen, wenn max_size überschritten wird
    buffer.append(value)
    if len(buffer) > max_size:
        buffer.pop(0)  # Entfernt den ältesten Wert
    buffer = sum(buffer) / len(buffer) if buffer else 0
    # print('B', buffer)
    return buffer


def battery_measure():
    global battery_val
    # Lese Joystickwerte und mappe auf Bereich -100 bis +100
    voltage = Battery_Voltage.read_battery_voltage(adc.read())
    voltage = average_val(battery_val, voltage)
    return voltage


def battery_percent(voltage):
    percentage = Battery_Voltage.calculate_battery_percentage(voltage)
    return percentage


def battery_to_controller_command(voltage, percentage):
    # print(f'Batteriespannung: {voltage}, Ladestand: {percentage}')
    return f"{int(round(voltage, 1) * 1000)},{percentage}"


# Callback für empfangene ESP-NOW-Nachrichten
def on_receive(mac, message, percentage):
    if message != None:
        command = message.decode('utf-8')
        x_cmd, y_cmd = map(int, command.split(","))
        print(f"Empfangener Befehl: Lenkung {x_cmd}, Geschwindigkeit {y_cmd}")

        # Steuere das Auto basierend auf den empfangenen Daten
        if percentage < 1:
            steer_car(0)
            drive_car(0)
        else:
            steer_car(x_cmd)
            if y_cmd > -10 and y_cmd < 10:
                y_cmd = 0
            drive_car(y_cmd)


def peer_connection(msg, voltage, percentage):
    # Überprüft ob vom Auto Nachrichten kommen
    global counter
    if counter > 6:
        counter = 0
    else:
        counter += 1
    if msg == None:
        lcd.move_to(0, 1)
        if percentage > 0:
            if counter > 3:
                lcd.putstr(f"No connection  -")
            else:
                lcd.putstr(f"No connection - ")
        else:
            if counter > 3:
                lcd.putstr(f"No connection   ")
            else:
                lcd.putstr(f"Battery low!   ")
    else:
        lcd.move_to(0, 1)
        if percentage < 1:
            lcd.putstr(f"Battery low!   ")
        else:
            lcd.putstr(f"                ")
        esp.irq(on_receive(host, msg, percentage))
    lcd.move_to(0, 0)
    if percentage > 0:
        lcd.putstr(f"Batt: {round(voltage, 1)}V  {percentage}%")
    else:
        lcd.putstr(f"Batt: {round(voltage, 1)}V  {percentage}%  ")


print("Auto ist bereit, Befehle zu empfangen.")

try:
    while True:
        batt_v = battery_measure()
        batt_p = battery_percent(batt_v)
        command = battery_to_controller_command(batt_v, batt_p)
        # print(batt_v)

        esp.send(CONTROLLER_MAC, command.encode('utf-8'))
        time.sleep_ms(20)  # Ruhemodus, das Empfangen läuft über den Callback
        host, msg = esp.recv(200)
        peer_connection(msg, batt_v, batt_p)
        esp.irq(on_receive(host, msg, batt_p))
except:
    lcd.clear()
    pass