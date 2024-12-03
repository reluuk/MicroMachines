# IT Projekt RC-Auto 
#### Team Micromachines: Lukas Reif, David Wolf, Niklas Bräu

## Tätigkeitsnachweis:
### KW44: 
    -Bestellung Einzelteile(ESP32-Frenove Kits, Batteriehalter,H-Brücken, Joysticks etc.)
    -Bestellung des RC-Auto Bausatz
    -erstes Mal ESP32 angeschlossen und LEDs blinken lassen

### KW45: 
    -Auslesen der Mac-Adressen für ESP-NOW
    -Stecken der Schaltung zum Auslesen der Joysticks

### KW46: 
#### Zusammenbau des RC-Auto Bausatzes:

    -Stecken der Schaltung zur Ansteuerung des Servomotors
        -Erweiterung der Schaltung mit einen Joystick zur Ansteuerung

    -Bau eines Prototypen Controller aus Basteholz
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
    -Batteriewerte des Autos am Controller anzeigen lassen:
        -Batteriespannungsmessung(V) und Kapazitätsumwandlung(%) am Auto umgesetzt (Reif)
        -Batteriewerte vom Auto an Controller mit ESP-NOW schicken lassen (Reif)
        -Batteriewerte auf mini OLED Display angezeigt (Reif)
                                                  
      

    
