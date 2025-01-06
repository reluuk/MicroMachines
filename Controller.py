import network
import espnow
from machine import ADC, Pin, I2C
import time
from ssd1306 import SSD1306_I2C

# Potentiometer links
adc = ADC(Pin(35))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

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

counter = 0
forwards_reverse_val = []
right_left_val = []
potetiometer_val = []


def joystick_to_motor_command_forwards_backwards(adcValue):
    global forwards_reverse_val
    # Lese Joystickwerte und mappe auf Bereich -100 bis +100
    y_val = y_joystick.read()
    y_cmd = int((average_val(forwards_reverse_val, y_val, 3) - 2048) / 20.48)
    pwmValue = poti(adcValue)
    y_cmd = scale_forward_reverse_value(pwmValue, y_cmd)
    if y_cmd > 100:
        y_cmd = 100
    elif y_cmd < -100:
        y_cmd = -100
    elif y_cmd > -15 and y_cmd < -10:
        y_cmd = 0
    print(y_cmd)
    return y_cmd


def joystick_to_motor_command_left_right():
    global right_left_val
    # Lese Joystickwerte und mappe auf Bereich -100 bis +100
    x_val = x_joystick.read()
    print(x_val)
    x_cmd = int((average_val(right_left_val, x_val, 3) - 2048) / 20.48)
    if x_cmd < -10 and x_cmd > -15:
        x_cmd = 0
    return x_cmd * -1


def joystick_to_motor_command(y_cmd, x_cmd):
    return f"{x_cmd},{y_cmd}"


def scale_forward_reverse_value(adc1_value, adc2_raw):
    # Bereich von ADC2 abhängig von ADC1 berechnen
    # adc1_scaled = adc1_value / 1023 * 100  # Skalieren von 0-1023 auf 0-100
    range_min = -55 - (adc1_value * 70 / 100)
    range_max = 60 + (adc1_value * 70 / 100)

    # ADC2-Wert von 0-1023 auf range_min - range_max skalieren
    adc2_scaled = range_min + ((adc2_raw + 100) / 200) * (range_max - range_min)
    return int(adc2_scaled)


def on_receive(mac, message):
    command = message.decode('utf-8')
    battery_v, battery_per = map(int, command.split(","))
    battery_v = round(battery_v / 1000, 2)
    # print(f"Empfangen: Batteriespannung {battery_v}, Ladezustand {battery_per}")

    display.text(f'batt: {battery_v}V  {battery_per}%', 0, 0, 1)
    # display.text(f'{battery_per}%', 0, 10, 1)
    # display.show()


def average_val(buffer, value, max_size=50):
    # Wert zur Liste hinzufügen und älteste Werte entfernen, wenn max_size überschritten wird
    buffer.append(value)
    if len(buffer) > max_size:
        buffer.pop(0)  # Entfernt den ältesten Wert
    buffer = sum(buffer) / len(buffer) if buffer else 0
    # print('B', buffer)
    return buffer


def peer_connection(msg, poti_val, y_cmd, x_cmd):
    # Überprüft ob vom Auto Nachrichten kommen
    global counter
    if counter > 50:
        counter = 0
    else:
        counter += 1
    poti_ = poti(poti_val)
    if msg == None:
        display.fill(0)
        display.text('No Connection', 10, 0 + counter, 1)
        display.text(f'{y_cmd}', 0, 20, 1)
        display.text(f'{x_cmd}', 0, 30, 1)
        display.text(f'{poti_}', 0, 40, 1)
        display.show()

    else:
        display.text(f'Power:     {poti_}%', 0, 10, 1)
        display.text(f'fwrd/rev:  {y_cmd}', 0, 20, 1)
        display.text(f'left/right:{x_cmd}', 0, 30, 1)
        esp.irq(on_receive(host, msg))


def remap(value, oldMin, oldMax, newMin, newMax):
    return int((value) * (newMax - newMin) / (oldMax - oldMin))


def poti(adcValue):
    global potetiometer_val
    pwmValue = remap(average_val(potetiometer_val, adcValue, 3), 0, 4095, 0, 100)
    return pwmValue


try:
    while True:
        display.fill(0)  # fill entire screen with colour=0
        y_val = joystick_to_motor_command_forwards_backwards(adc.read())
        x_val = joystick_to_motor_command_left_right()
        print(x_val)
        command = joystick_to_motor_command(y_val, x_val)
        esp.send(AUTO_MAC, command.encode('utf-8'))  # Sende die Joystickdaten an das Auto
        # print(f"Gesendeter Befehl: {command}")
        host, msg = esp.recv(100)
        peer_connection(msg, adc.read(), y_val, x_val)
        display.show()
        time.sleep_ms(10)  # Sende alle 10ms
except:
    display.fill(0)
    display.show()
    pass