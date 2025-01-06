from machine import ADC, Pin
import time

'''# Konfiguration für den ADC
adc = ADC(Pin(32))         # ADC an GPIO 34
adc.width(ADC.WIDTH_12BIT)  # 12-bit Auflösung (0-4095)
adc.atten(ADC.ATTN_11DB)    # 11dB Attenuation -> max ~3.6V'''

class Battery_Voltage:
    
    def read_battery_voltage(a):
        # Spannungsteiler-Verhältnis
        R1 =  29500  # Widerstand R1 in Ohm
        R2 =  9500  # Widerstand R2 in Ohm
        divider_ratio = (R1 + R2) / R2
        
         # Korrekturfaktor für die Spannung (wenn Abweichung prozentual ist)
        CALIBRATION_FACTOR_1 = 3.065/3.28  # Korrekturfaktor links: tatsächlicher Wert, rechts: gemessener Wert
        CALIBRATION_FACTOR_2 = 12.2/12.56  # Korrekturfaktor links: tatsächlicher Wert, rechts: gemessener Wert
        # Offset für die Spannung (wenn Abweichung konstant ist)
        OFFSET = 0.9  # Unterschied zwischen gemessener und tatsächlicher Spannung
        
        raw_value = a        # ADC-Wert lesen
        #print(raw_value)
        measured_voltage = (raw_value / 4095 * 3.3) * CALIBRATION_FACTOR_1 # Umrechnen auf 3.3V Skala
        #print(measured_voltage)
        battery_voltage = (measured_voltage * divider_ratio) * CALIBRATION_FACTOR_2 # Kalibrierung anwenden
        #battery_voltage = battery_voltage - OFFSET # Offset anwenden
        return battery_voltage  # Umrechnen mit Spannungsteiler

    def calculate_battery_percentage(voltage):
        # LiPo Batterie-Schwellenwerte
        FULL_BATTERY_VOLTAGE = 12.6  # Volle Spannung (3S LiPo)
        EMPTY_BATTERY_VOLTAGE = 10.0  # Leere Spannung (3S LiPo)
        
        # Ladezustand berechnen
        if voltage >= FULL_BATTERY_VOLTAGE:
            return 100
        elif voltage <= EMPTY_BATTERY_VOLTAGE:
            return 0
        else:
            return int((voltage - EMPTY_BATTERY_VOLTAGE) / (FULL_BATTERY_VOLTAGE - EMPTY_BATTERY_VOLTAGE) * 100)

# Hauptschleife
'''while True:
    #print(adc.read())
    #readvoltage = Battery_Voltage
    voltage = Battery_Voltage.read_battery_voltage(a = adc.read())
    percentage = Battery_Voltage.calculate_battery_percentage(voltage)
    print("Batteriespannung: {:.2f}V, Ladezustand: {}%".format(voltage, percentage))
    time.sleep(2)  # Alle 2 Sekunden aktualisieren'''
