# Öffnet das jeweilige Programm, wenn das ESP32 mit Strom versorgt wird
with open('Controller.py') as file:  # Das auszuführende Programm in die Klammer
    exec(file.read())