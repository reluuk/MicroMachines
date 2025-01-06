# Dokumentation Micromachines

**Mitglieder:**
- Lukas Reif
- Niklas Bräu
- David Wolf

## KW44 _(28.10. - 03.11.2024)_
### Aktivitäten:
- Bestellung Einzelteile(ESP32-Frenove Kits, Batteriehalter,H-Brücken, Joysticks etc.) (Bräu)
- Bestellung RC-Auto Bausatz (Wolf)
- erstes Mal ESP32 angeschlossen und LEDs blinken lassen (Reif)
### Code:
LED blinken lassen

    import time
    from machine import Pin
    led = Pin(45, Pin.OUT)
    while True:
        led.on()
        time.sleep_ms(100)
        led.off()
        time.sleep_ms(100)

## KW45 _(04. - 10.11.2024)_
### Aktivitäten:
- Auslesen der Mac-Adressen für ESP-NOW (alle)
- Probieren der Kommunikation zwischen den ESP32 (alle)
- Stecken der Schaltung zum Auslesen der Joysticks (Bräu)
### Code:
Joystick auslesen:
    from machine import ADC, Pin
    import time

    # Initialisierung der analogen Pins für X- und Y-Achse
    x_pin = ADC(Pin(32))  # Pin für X-Achse
    y_pin = ADC(Pin(33))  # Pin für Y-Achse

    # Setze die Auflösung für die analogen Eingänge (optional)
    x_pin.atten(ADC.ATTN_11DB)  # Bereich von 0 bis 3,6V
    y_pin.atten(ADC.ATTN_11DB)  # Bereich von 0 bis 3,6V

    # Initialisierung des digitalen Pins für den Button (optional)
    #button_pin = Pin(32, Pin.IN, Pin.PULL_UP)

    # Hauptschleife
    while True:
        # Lesen der X- und Y-Achsenwerte
        x_value = x_pin.read()
        y_value = y_pin.read()

        # Lesen des Button-Status
        #button_pressed = not button_pin.value()  # Taster ist gedrückt, wenn Wert 0

        # Ausgabe der Werte
        print("X-Achse:", x_value)
        print("Y-Achse:", y_value)
        #print("Button gedrückt:", button_pressed)

        # Warte eine kurze Zeit, um die Anzeige lesbar zu machen
        time.sleep(0.1)

Mac-Adresse auslesen

    import network

    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    
    wlan_mac = wlan_sta.config('mac')
    print("MAC Address:", wlan_mac)  # Show MAC for peering
ESP-NOW Sender

    import network
    import espnow
    
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.WLAN.IF_STA)  # Or network.WLAN.IF_AP
    sta.active(True)
    sta.disconnect()      # For ESP8266
    
    e = espnow.ESPNow()
    e.active(True)
    peer = b'\xbb\xbb\xbb\xbb\xbb\xbb'   # MAC address of peer's wifi interface
    e.add_peer(peer)      # Must add_peer() before send()
    
    e.send(peer, "Starting...")
    for i in range(100):
        e.send(peer, str(i)*20, True)
    e.send(peer, b'end')
ESP-NOW Receiver

    import network
    import espnow
    
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.WLAN.IF_STA)
    sta.active(True)
    sta.disconnect()   # Because ESP8266 auto-connects to last Access Point
    
    e = espnow.ESPNow()
    e.active(True)
    
    while True:
        host, msg = e.recv()
        if msg:             # msg == None if timeout in recv()
            print(host, msg)
            if msg == b'end':
                break
### Quellen:
- [ESP32 Mac-Adresse auslesen]https://stackoverflow.com/questions/71902740/how-to-retrieve-and-format-wifi-mac-address-in-micropython-on-esp32
- [ESP-NOW Tutorial]https://docs.micropython.org/en/latest/library/espnow.html
- [Joystick auslesen]nicht auffindbar/nicht in ChatGPT gefunden
## KW46 _(11. - 17.11.2024)_
### Aktivitäten:
- Zusammenbau des RC-Autobausatzes (alle)
- Stecken der Schaltung zur Ansteuerung des Servomotors (Bräu)
  - Erweiterung der Schaltung mit einem Joystick zur Ansteuerung
- Bau eines Prototyps Controller aus Bastelholz (Bräu)
  - Montieren vom Steckbrett mit ESP 32 und Joysticks auf den Prototypen
### Code:

Servo-Motor Ansteuerung per Joystick:

    from machine import ADC, Pin, PWM
    import time

    y_pin = ADC(Pin(33))
    y_pin.atten(ADC.ATTN_11DB)  # Bereich von 0 bis 3,6V für den ADC

    servo_pin = PWM(Pin(4), freq=50)  # 50 Hz ist die übliche Frequenz für Servos

    servo_min = 47    # Minimaler Duty-Wert (0°)
    servo_max = 95    # Maximaler Duty-Wert (180°)

    def map_value(value, in_min, in_max, out_min, out_max):
        """Skaliert den Wert von einem Bereich auf einen anderen."""
        return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    while True:
        # Lese den Wert der Y-Achse
        y_value = y_pin.read()
    
        # Mappe den Y-Achsen-Wert auf den Bereich des Servos
        # Annahme: ADC-Wertbereich ist 0 bis 4095
        servo_value = map_value(y_value, 0, 4095, servo_min, servo_max)
    
    # Setze den Servo-Winkel
    servo_pin.duty(servo_value)
    
    # Ausgabe für Debugging
    print("Y-Achse:", y_value, "Servo-Wert:", servo_value)
    
    # Wartezeit für Stabilität
    time.sleep(0.2)

### Quellen:
- [Niklas]:nicht auffindbar/nicht in ChatGPT gefunden
## KW47 _(18. - 24.11.2024)_
### Aktivitäten:
- Montage der Schaltung zur Ansteuerung vom RC-Auto auf den Auto (Bräu)
  - Verdrahtung der Schaltung mit Motor und Servo-Motor
  - Einbindung vom Akku in die Schaltung
  - Aufspielen des Programms auf das ESP 32
- Inbetriebnahme des Controllers (Bräu)
  - Aufspielen des Programms auf das ESP 32
- Erster Test der Programme Car und Controller (Reif)
- Erste Testfahrt mit dem Auto (Wolf)
  - Reichweite getestet
  - Ansteuerung getestet(Lenkung,Vorwärts/Rückwärts)

  Ergebnis: beide Punkte i.O
### Probleme und Lösungen:
- Räder waren schief aufgesetzt dadurch drall nach rechts
  - Räder demontiert, Kugellager sind nicht gleich tief innerhalb der Lenkarme
  - keine einwandfreie Lösung für drall nach rechts durch Qualität der Lenkung
- Steuerung durch die Joysticks war invertiert
  - Joysticks wurden um 180° gedreht
- while Schleife im Car.py Code hat nicht funktioniert
  - Ablauf in den while Schleife korrigiert
- servo.duty bekommt negativen Wert
  - duty kann keine negativen Werte annehmen, Werte werden im Programm auf Servo-Winkel umgerechnet
- Servo und ESP32 dürfen nicht an gleicher 5V Quelle der H-Brücke angeschlossen werden
  - Provisorisch wurde das ESP32 mit einer seperaten Batterie betrieben
### Code:
- Siehe git history
### Quellen:
- ChatGPT: wie passe ich ein joystick signal von 0 bis 4096 auf ein servowert von 40-140 an
## KW48 _(25.11. - 01.12.2024)_
### Aktivitäten:
- Erstellen eines GitHub-Repository (Reif)
- Skizzieren eines Controller-Layouts zur zukünftigen Planung (Bräu)
- Erstellen einer Mindmap zur Projektzielübersicht (Bräu)
- Anpassung der Radstellung an der Lenkeraufhängung (Wolf)
- Anpassung der Servo Einstellung im Car Programm (Reif + Wolf)
### Probleme und Lösungen:
- die Joysticks liefern an ihrer eigentlichen Nullstellung nicht den erwarteteten Wert 0
- der Wert schwankt stark zwischen -8 und 5, somit wird im Code der Wertebereich 0 zugewiesen
### Code:
        if y_cmd > -10 and y_cmd < 10:
        y_cmd = 0
## KW49 _(02. - 08.12.2024)_
### Aktivitäten:
- Automatisches ausführen der Car und Controller Programme mit boot.py auf den ESP32
- Entwicklung einer benutzerdefinierten Platine für den Controller (Bräu)
- Entwicklung des Codes um Batteriewerte des Autos am Controller anzeigen lassen: (Reif) 
    - Batteriespannungsmessung(V) und Kapazitätsumwandlung(%) -> measure_Class.py erstellt 
    - Batteriewerte werden vom Auto an Controller mit ESP-NOW geschickt
    - Batteriewerte auf mini OLED Display angezeigt -> ssd1306.py erstellt
- Entwicklung der Schaltung um 12V LiPo Batterie mit ESP32 zu messen: (Wolf)
    - Spannungsteiler mit R1 = 30kΩ und R2 = 10kΩ
    - ESP32 wird parallel zu R2 angeschlossen
- Verbindungsstatus ESP-NOW wird auf OLED Display angezeigt (Reif) 
- die Kraft des Motors mit einem Potentiometer am Controller regeln (Reif) 
### Probleme und Lösungen:
- nicht alle GPIO Pins können einwandfrei eine Spannung messen, GPIO Pin 32 wurde ausgewählt
- die vom ESP32 gemessene Spannung am Spannungsteiler passt nicht zu der Eingangsspannung
  - ein Kalibrationsfaktor hilft den vom ESP32 gemessenen Wert an den tatsächlichen Wert anzupassen
- die gemessenen Spannungswerte schwanken zu schnell, kein eindeutiger Wert ablesbar
  - der Durchschnittswert der letzten 50 gemessenen Spannungswerte wird angezeigt
### Code:
- Siehe git history
### Quellen:
- ChatGPT: wie lässt man ein python programm ein anderes python file ausführen?
- ChatGPT: spannung einer 12v 3s lipo batterie messen und ladezustand anzeigen mit esp32 und micropython
  - Das Programm rechnet die gemessene Spannung nicht richtig auf die Eingangsspannung um, bei gemessen: 2,6V gibt es 10,6V aus aber es sollten 12,2V sein
  - wie lasse ich aus den letzten 20 gemessenen Werten einen Durchschnittswert errechnen
- ChatGPT: wie lasse ich ein 0.96 inch OLED SSD1306 display I2C 128 x 64 pixels Display mit einem ESP32 mit micropython werte anzeigen?
  - was kann ich alles damit machen und kann ich die Schriftgöße und art ändern?
- ChatGPT: Ich möchte in micropython mit einem esp32 einen adc1 wert der auf 0 bis 100 umgerechnet wurde einfluss nehmen lassen auf einen adc2 wert der von -100 bis 100 geht. der adc2 wert soll so skaliert werden, dass wenn adc1 0 hat der adc2 wert von -30 bis 30 geht und wenn adc1 100 ist ad2 von -100 bis 100 geht
  - passt nicht, zur info der adc2 wird auch ausgelesen und schon vorher auf -100 bis 100 skaliert
  - guter ansatz, ich möchte aber wenn adc1 0 ist das adc2 -100 bis 100 auf adc2 -30 bis 30 umgerechnet wird um den vollen wertebereich auszuschöpfen

- [OLED library]https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py
## KW50 _(09. - 15.12.2024)_
### Aktivitäten:
- Zielsetzung:
  - das Auto wird fest verdrahtet/verlötet (Reif)
  - das Auto bekommt noch eine LCD-Anzeige für den Batteriestatus und zur Überprüfung der ESP-NOW Verbindung
  - der Controller wird noch fertiggestellt (Bräu)
  - eine benutzerdefinierte Platine für den Controller wird nicht mehr bestellt, wegen zu langer Lieferzeit

- Erste Lötarbeiten am Auto erledigt (Reif)
### Code:
- Siehe git history
### Quellen:
- [LCD libraries]https://github.com/Freenove/Freenove_ESP32_WROOM_Board/tree/main/Python/Python_Libraries
## KW51 _(16. - 22.12.2024)_
### Aktivitäten:
- Lötarbeiten am Auto: (Reif)
  - Steckplatz für ESP32 auf Lochrasterplatine angebracht
  - Feinsicherungen als Kurzschlussschutz für Batterie in Schaltkreis integriert
  - An/Aus Schalter von Chassis-Kit in Schaltkreis integriert
### Probleme und Lösungen:
- der 5V Ausgang der H-Brücke am Auto kann nur 500mA (78M05) liefern, das ist zu wenig um damit den Servo und ESP32 mit Spannung zu versorgen
  - da mehrere H-Brücken bestellt wurden, wurde der 5V Spannungsregler (78M05) einer H-Brücke auf eine extra Lochrasterplatine gelötet, das wird die Spannungsversorgung für den Servo
  - Online Schaltplan der H-Brücke war komplett falsch, ChatGPT liefert einen richtigen Schaltplan
### Quellen:
- [H-Brücke]https://components101.com/modules/l293n-motor-driver-module
- [Datenblatt Spannungsregler 78M05]https://www.digikey.de/de/products/detail/umw/78M05/17635217
- ChatGPT: wie regele ich eine spannung von 12v auf 5v mit einem 78m05
## KW52 _(23. - 29.12.2024)_
### Aktivitäten:
- Lötarbeiten am Auto: (Reif)
  - Spannungsteiler für Batteriespannungsmessung auf ESP32-Platine angebracht
  - PCB-Schraubklemmen für Anschluss der Komponenten auf ESP32-Platine angebracht
  - Verbindungen von PCB-Schraubklemmen zu ESP32 an der ESP32-Platine mit Kupferlackdraht erstellt

- ESP32-Platine, H-Brücke, DC Motor, Servo Motor, 5V Platine, LCD und Batterie verdrahtet
## KW1 (30.12.2024 - 05.01.2025)
### Aktivitäten:
- Erstellen eines Videoclips für die Präsentation (Bräu)
## KW2 (06.01.2025)
### Aktivitäten:
- Letzte Feineinstellung am Auto (Reif + Bräu)
- Fertigstellung der Dokumentation (Wolf)
