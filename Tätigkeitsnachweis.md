# Dokumentation Micromachines

**Mitglieder:**
- Lukas Reif
- Niklas Bräu
- David Wolf

## KW44
### Aktivitäten:
    -Bestellung Einzelteile(ESP32-Frenove Kits, Batteriehalter,H-Brücken, Joysticks etc.) (Bräu)
    -Bestellung des RC-Auto Bausatz (Bräu)
    -erstes Mal ESP32 angeschlossen und LEDs blinken lassen (Reif)
### Code:
    import time
    from machine import Pin
    led = Pin(45, Pin.OUT)
    while True:
        led.on()
        time.sleep_ms(100)
        led.off()
        time.sleep_ms(100)

## KW45
### Aktivitäten:
    -Auslesen der Mac-Adressen für ESP-NOW (alle)
    -Probieren der Kommunikation zwischen den ESP32 (alle)
    -Stecken der Schaltung zum Auslesen der Joysticks (Bräu)
### Code1:
    import network

    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    
    wlan_mac = wlan_sta.config('mac')
    print("MAC Address:", wlan_mac)  # Show MAC for peering
### Code2:
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
### Code3:
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
    https://stackoverflow.com/questions/71902740/how-to-retrieve-and-format-wifi-mac-address-in-micropython-on-esp32
    https://docs.micropython.org/en/latest/library/espnow.html
## KW46
### Aktivitäten:
    -Zusammenbau des RC-Auto Bausatzes (alle)
    -Stecken der Schaltung zur Ansteuerung des Servomotors (Bräu)
        -Erweiterung der Schaltung mit einen Joystick zur Ansteuerung
    -Bau eines Prototypen Controller aus Basteholz (Bräu)
        -Montieren vom Steckbrett mit ESP 32 und Joysticks auf den Prototypen
### Code:
[Niklas]
### Quellen:
[Niklas]
## KW47
    -Montage der Schaltung zur Ansteuerung vom RC-Auto auf den Auto (Bräu)
        -Verdrahtung der Schaltung mit Motor und Servo-Motor
        -Einbindung vom Akku in die Schaltung
        -Aufspielen des Programms auf das ESP 32
     
      
    -Inbetriebnahme des Controllers (Bräu)
        -Aufspielen des Programms auf das ESP 32

    -Erster Test der Programme Car und Controller (Reif)
        -while Schleife korrigiert im Car Programm
        -servo.duty bekommt negativen Wert -> Fehler
        -Servo und ESP32 dürfen nicht an gleicher 5V Quelle der H-Brücke angeschlossen werden
        

    -Erste Testfahrt mit dem Auto (Wolf)
        Test: 
            -Reichweite getestet
            -Ansteuerung getestet(Lenkung,Vorwärts/Rückwärts)

            Ergebnis: beide Punkte i.O
### Probleme und Lösungen:
    -Räder waren schief aufgesetzt -> dadurch drall nach Rechts
    -Steuerung durch die Joysticks war invertiert
    -while Schleife im Car.py Programm korrigiert, ChatGPT hat die Reihenfolge durcheinander gebracht
    -servo.duty bekommt negativen Wert -> Fehler
    -Servo und ESP32 dürfen nicht an gleicher 5V Quelle der H-Brücke angeschlossen werden, kann nur 500mA liefern
### Code:
- Siehe git history
### Quellen:
[Niklas]
## KW48
    -Erstellen eines GitHub-Repository (Reif)
    -Skizzieren eines Controller Layouts zur zukünftigen Planung (Bräu)
    -Erstellen einer Mindmap zur Projektzielübersicht (Bräu)
    -Anpassung der Radstellung an der Lenkeraufhängung (Wolf)
    -Anpassung der Servo Einstellung im Car Programm (Reif + Wolf)
### Probleme und Lösungen:
    -die Joysticks liefern an ihrer eigentlichen Nullstellung nicht den erwarteteten Wert 0
    -der Wert schwankt stark zwischen -8 und 5, somit wird im Code der Wertebereich 0 zugewiesen
### Code:
        if y_cmd > -10 and y_cmd < 10:
        y_cmd = 0
## KW49
    -Entwicklung einer benutzerdefinierten Platine für den Controller (Bräu)
    -Entwicklung des Codes um Batteriewerte des Autos am Controller anzeigen lassen: (Reif) 
        -Batteriespannungsmessung(V) und Kapazitätsumwandlung(%) -> measure_Class.py erstellt 
        -Batteriewerte werden vom Auto an Controller mit ESP-NOW geschickt
        -Batteriewerte auf mini OLED Display angezeigt -> ssd1306.py erstellt
    -Entwicklung der Schaltung um 12V LiPo Batterie mit ESP32 zu messen: (Wolf)
        -Spannungsteiler mit R1 = 30kΩ und R2 = 10kΩ
        -ESP32 wird parallel zu R2 angeschlossen
    -Verbindungsstatus ESP-NOW wird auf OLED Display angezeit

## KW50
    Zielsetzung:
        -das Auto wird fest verdrahtet/verlötet (Reif)
        -das Auto bekommt noch eine LCD-Anzeige für den Batteriestatus und zur Überprüfung der ESP-NOW Verbindung
        -der Controller wird noch fertig gestellt (Bräu)
        -eine benutzerdefinierte Platine für den Controller wird nicht mehr bestellt, wegen zu langer Lieferzeit
    
    -Erste Lötarbeiten am Auto erledigt (Reif)

## KW51
    Problem:
        -5V Ausgang der H-Brücke am Auto kann nur 500mA liefern, das ist zu wenig um damit den Servo und ESP32 laufen zu lassen
    Lösung:
        -da mehrere H-Brücken bestellt wurden, wird der 5V Spannungsteil einer H-Brücke auf einer extra Lochrasterplatine verlötet
        -das wird die Spannungversogung für den Servo
    
    Lötarbeiten am Auto:
        -Steckplatz für ESP32 auf Lochrasterplatine angebracht
        -Feinsicherungen als Kurzschlussschutz für Batterie in Schaltkreis integriert
        -An/Aus Schalter von Chassis-Kit in Schaltkreis integriert

## KW52
    Lötarbeiten am Auto:
        -Spannungteiler für Batteriespannungsmessung auf ESP32-Platine angebracht
        -PCB-Schraubklemmen für Anschluss der Komponenten auf ESP32-Platine angebracht
        -Verbindungen von PCB-Schraubklemmen zu ESP32 an der ESP32-Platine mit Kupferlackdraht erstellt

    -Verbindungen der ESP32-Platine, H-Brücke, DC Motor, Servo Motor, 5V Platine, LCD und Batterie mit Verdrahtungsleitungen erstellt
    Auto fertig gestellt