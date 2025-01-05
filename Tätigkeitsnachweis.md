# IT Projekt RC-Auto 
#### Team Micromachines: Lukas Reif, David Wolf, Niklas Bräu

## Tätigkeitsnachweis:
### KW44: 
    -Bestellung Einzelteile(ESP32-Frenove Kits, Batteriehalter,H-Brücken, Joysticks etc.) (Bräu)
    -Bestellung des RC-Auto Bausatz (Bräu)
    -erstes Mal ESP32 angeschlossen und LEDs blinken lassen (Reif)

### KW45: 
    -Auslesen der Mac-Adressen für ESP-NOW (Reif)
    -Stecken der Schaltung zum Auslesen der Joysticks (Bräu)

### KW46: 
#### Zusammenbau des RC-Auto Bausatzes:

    -Stecken der Schaltung zur Ansteuerung des Servomotors (Bräu)
        -Erweiterung der Schaltung mit einen Joystick zur Ansteuerung

    -Bau eines Prototypen Controller aus Basteholz (Bräu)
        -Montieren vom Steckbrett mit ESP 32 und Joysticks auf den Prototypen

### KW47: 
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
    ___________________________________________________________________

        Probleme: 
            -Räder schief aufgesetzt -> dadurch drall nach Rechts
            -Steuerung durch die Joysticks war invertiert

### KW48: 
    -Erstellen eines GitHub-Repository (Reif)
    -Skizzieren eines Controller Layouts zur zukünftigen Planung (Bräu)
    -Erstellen einer Mindmap zur Projektzielübersicht (Bräu)
    -Anpassung der Radstellung an der Lenkeraufhängung (Wolf)
    -Anpassung der Servo Einstellung im Car Programm (Reif)

### KW49:
    -Entwicklung einer benutzerdefinierten Platine für den Controller (Bräu)
    -Entwicklung des Codes um Batteriewerte des Autos am Controller anzeigen lassen: (Reif) 
        -Batteriespannungsmessung(V) und Kapazitätsumwandlung(%) -> measure_Class.py erstellt 
        -Batteriewerte werden vom Auto an Controller mit ESP-NOW geschickt
        -Batteriewerte auf mini OLED Display angezeigt -> ssd1306.py erstellt
    -Entwicklung der Schaltung um 12V LiPo Batterie mit ESP32 zu messen: (Wolf)
        -Spannungsteiler mit R1 = 30kΩ und R2 = 10kΩ
        -ESP32 wird parallel zu R2 angeschlossen

### KW50:
    Zielsetzung:
        -das Auto wird fest verdrahtet/verlötet (Reif)
        -das Auto bekommt noch eine LCD-Anzeige für die Batteriespannung und zur Überprüfung der ESP-NOW Verbindung
        -der Controller wird noch fertig gestellt (Bräu)
        -eine benutzerdefinierte Platine für den Controller wird nicht mehr bestellt, wegen zu langer Lieferzeit
    
    -Erste Lötarbeiten am Auto erledigt (Reif)

### KW51:
    Problem:
        -5V Ausgang der H-Brücke am Auto kann nur 500mA liefern, das ist zu wenig um damit den Servo und ESP32 laufen zu lassen
    Lösung:
        -da mehrere H-Brücken bestellt wurden, wird der 5V Spannungsteil einer H-Brücke auf einer extra Lochrasterplatine verlötet
        -das wird die Spannungversogung für den Servo
    
    Lötarbeiten am Auto:
        -Steckplatz für ESP32 auf Lochrasterplatine angebracht
        -Feinsicherungen als Kurzschlussschutz für Batterie in Schaltkreis integriert
        -An/Aus Schalter von Chassis-Kit in Schaltkreis integriert

### KW52:
    Lötarbeiten am Auto:
        -Spannungteiler für Batteriespannungsmessung auf Lochrasterplatine angebracht
        -PCB-Schraubklemmen für Anschluss der Komponenten an ESP32 auf Lochrasterplatine angebracht
        -Verbindungen von PCB-Schraubklemmen zu ESP32 an der Lochrasterplatine mit Kupferlackdraht erstellt
        -Verbindungen der ESP32 Platine, H-Brücke, DC Motor, Servo Motor, 5V Platine, LCD und Batterie mit Verdrahtungsleitungen erstellt
    Auto fertig gestellt